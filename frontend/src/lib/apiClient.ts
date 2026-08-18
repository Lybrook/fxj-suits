type ApiResult<T> = { data: T | null; error: { message: string } | null };

type QueryFilter = { key: string; value: string };

const API_BASE = (process.env.NEXT_PUBLIC_DJANGO_API_URL || "/api/backend").replace(/\/$/, "");
const TOKEN_KEY = "fxj-suits-api-token";

function getToken() {
  if (typeof window === "undefined") return "";
  return window.localStorage.getItem(TOKEN_KEY) || "";
}

function setToken(token: string | null) {
  if (typeof window === "undefined") return;
  if (token) window.localStorage.setItem(TOKEN_KEY, token);
  else window.localStorage.removeItem(TOKEN_KEY);
}

async function request<T>(path: string, init: RequestInit = {}): Promise<ApiResult<T>> {
  try {
    const headers = new Headers(init.headers);
    const token = getToken();
    if (token) headers.set("Authorization", `Token ${token}`);
    if (init.body && !(init.body instanceof FormData)) headers.set("Content-Type", "application/json");
    const response = await fetch(`${API_BASE}${path}`, {
      ...init,
      headers,
      credentials: "include",
      cache: "no-store",
    });
    const raw = await response.text();
    const body = raw ? JSON.parse(raw) : null;
    if (!response.ok) {
      return { data: null, error: { message: body?.detail || body?.message || `Request failed (${response.status})` } };
    }
    return { data: body as T, error: null };
  } catch (error) {
    return { data: null, error: { message: error instanceof Error ? error.message : "Network request failed" } };
  }
}

class QueryBuilder<T = any> implements PromiseLike<ApiResult<T>> {
  private operation: "select" | "insert" | "upsert" | "update" | "delete" = "select";
  private payload: any;
  private filters: QueryFilter[] = [];
  private orderKey = "";
  private ascending = true;
  private limitValue?: number;
  private returnSingle = false;

  constructor(private readonly table: string) {}

  select(_columns = "*") {
    this.operation = this.operation === "select" ? "select" : this.operation;
    return this;
  }

  insert(payload: any) {
    this.operation = "insert";
    this.payload = payload;
    return this;
  }

  upsert(payload: any, _options?: Record<string, any>) {
    this.operation = "upsert";
    this.payload = payload;
    return this;
  }

  update(payload: any) {
    this.operation = "update";
    this.payload = payload;
    return this;
  }

  delete() {
    this.operation = "delete";
    return this;
  }

  eq(key: string, value: any) {
    this.filters.push({ key, value: String(value) });
    return this;
  }

  not(_key: string, _operator: string, _value: any) {
    // The Django endpoint already scopes role-based records; this compatibility
    // method keeps optional legacy notification filtering non-blocking.
    return this;
  }

  order(key: string, options: { ascending?: boolean } = {}) {
    this.orderKey = key;
    this.ascending = options.ascending !== false;
    return this;
  }

  limit(value: number) {
    this.limitValue = value;
    return this;
  }

  single() {
    this.returnSingle = true;
    return this;
  }

  async execute(): Promise<ApiResult<T>> {
    if (this.operation === "select") {
      const params = new URLSearchParams();
      this.filters.forEach(({ key, value }) => params.set(key, value));
      if (this.orderKey) {
        params.set("order", this.orderKey);
        params.set("ascending", String(this.ascending));
      }
      if (this.limitValue !== undefined) params.set("limit", String(this.limitValue));
      const result = await request<any[]>(`/records/${this.table}${params.toString() ? `?${params}` : ""}`);
      if (result.error) return result;
      const value: any = this.returnSingle ? (result.data?.[0] || null) : result.data;
      return { data: value as T, error: null };
    }

    if (this.operation === "insert" || this.operation === "upsert") {
      const result = await request<any>(`/records/${this.table}`, {
        method: "POST",
        body: JSON.stringify(this.payload),
      });
      if (result.error) return result;
      const value: any = this.returnSingle
        ? (Array.isArray(result.data) ? result.data[0] : result.data)
        : result.data;
      return { data: value as T, error: null };
    }

    const id = this.filters.find(filter => filter.key === "id")?.value;
    if (!id) return { data: null, error: { message: "An id filter is required for updates and deletes" } };
    const url = `/records/${this.table}/${encodeURIComponent(id)}`;
    const result = await request<any>(url, {
      method: this.operation === "update" ? "PATCH" : "DELETE",
      ...(this.operation === "update" ? { body: JSON.stringify(this.payload) } : {}),
    });
    return { data: result.data as T, error: result.error };
  }

  then<TResult1 = ApiResult<T>, TResult2 = never>(
    onfulfilled?: ((value: ApiResult<T>) => TResult1 | PromiseLike<TResult1>) | null,
    onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | null,
  ): Promise<TResult1 | TResult2> {
    return this.execute().then(onfulfilled, onrejected);
  }
}

class StorageBucket {
  constructor(private readonly bucket: string) {}

  async upload(path: string, file: File) {
    const form = new FormData();
    form.append("file", file);
    form.append("table", this.bucket);
    form.append("record_id", path.split("/")[0] || "");
    return request<{ url: string; id: string }>("/uploads", { method: "POST", body: form });
  }

  getPublicUrl(path: string) {
    if (path.startsWith("http://") || path.startsWith("https://")) return { data: { publicUrl: path } };
    const origin = API_BASE.endsWith("/api") ? API_BASE.slice(0, -4) : API_BASE;
    return { data: { publicUrl: `${origin}${path.startsWith("/") ? path : `/media/${path}`}` } };
  }
}

export const djangoClient = {
  from<T = any>(table: string) {
    return new QueryBuilder<T>(table);
  },
  storage: {
    from(bucket: string) {
      return new StorageBucket(bucket);
    },
  },
  auth: {
    async signInWithPassword({ email, password }: { email: string; password: string }) {
      const result = await request<{ token: string; user: any }>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      if (result.data?.token) setToken(result.data.token);
      return { data: result.data ? { session: { access_token: result.data.token }, user: result.data.user } : null, error: result.error };
    },
    async getSession() {
      const token = getToken();
      return { data: { session: token ? { access_token: token } : null }, error: null };
    },
    async getUser() {
      const result = await request<{ user: any }>("/auth/me");
      return { data: { user: result.data?.user || null }, error: result.error };
    },
    async signOut() {
      const result = await request<{ success: boolean }>("/auth/logout", { method: "POST" });
      setToken(null);
      return result;
    },
    onAuthStateChange(_callback: (event: string, session: any) => void) {
      return { data: { subscription: { unsubscribe() {} } } };
    },
  },
};

export { API_BASE };

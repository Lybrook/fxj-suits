import { djangoClient } from "./apiClient";

// Kept under the historical export name so existing screens can be migrated
// incrementally without duplicating their data access logic.
export const supabase = djangoClient;

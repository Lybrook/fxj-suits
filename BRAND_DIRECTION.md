# FXJ Suits Kenyan modernization direction

## Brand relationship

FXJ Suits is presented as a Kenyan legal-operations workspace powered by **Fikia × Jenga Tech**, a Kitale-based digital agency. The product identity remains FXJ Suits so the existing operational workflows do not lose continuity, while the login and shared shell make the relationship explicit: “FXJ Suits · Legal operations, powered by Fikia × Jenga Tech.”

## Kenyan localization

Use Kenyan English and Kenyan legal-operations language. Currency is Kenyan shillings (`KES` / `KSh`) with `en-KE` formatting. Default geographic examples should use Kenyan cities and counties, such as Nairobi, Kitale, Mombasa, Kisumu, Nakuru, and Kiambu. Replace non-Kenyan demo identities, Uganda-specific location defaults, UGX formatting, +256 phone values, and Uganda-specific registry references with neutral Kenyan court/registry terminology unless a field is explicitly generic or user-configurable. Kenyan sample records should be clearly marked as demo/sample data.

## Palette

Use the Fikia × Jenga visual language rather than the legacy brown/gold-only treatment:

| Token | Value | Use |
|---|---|---|
| Ink | `#17372C` | Primary navigation, headlines, primary text |
| Forest | `#27664D` | Brand accent, active states, positive emphasis |
| Sage | `#8AA79B` | Secondary surfaces, muted accents |
| Gold | `#D4B65D` | Warm highlight, key numbers, focus ring |
| Ivory | `#F7F6F1` | Main application canvas |
| White | `#FFFFFF` | Cards and elevated surfaces |
| Line | `#DDE5DD` | Borders and dividers |
| Muted | `#6F7F76` | Supporting text |

Retain the existing gold token as a compatibility alias where legacy pages reference it, but shift new shell styles to ink/forest/ivory/sage/gold so the app feels like the agency reference site rather than a dark brown template.

## Typography

Use a high-contrast editorial serif for display headings and a clean geometric sans for UI. The implementation loads `DM Sans` for navigation/body and `Cormorant Garamond` for large display headings, matching the reference site’s editorial and premium character without changing functional labels to decorative text.

## Layout and motion

The authenticated shell uses a dark forest sidebar, an ivory content canvas, soft white cards, and a slim context header. Motion is restrained and functional: shell fade-in, page entrance, active-nav pill transitions, hover lift, mobile sidebar slide, sync progress, and subtle hero/login floating accent cards. All non-essential motion is disabled under `prefers-reduced-motion`.

## Content hierarchy

The login experience should make the product’s purpose obvious within two seconds: Kenyan legal practice management, secure matter workflows, and a powered-by relationship with Fikia × Jenga Tech. The authenticated navigation should group the existing features into clear operational clusters without changing routes or role permissions.

## Preservation rule

Do not alter database schema, authentication flow, role guards, API contracts, or data-management semantics unless a strictly necessary localization change requires it. Prefer shared constants and formatting helpers over repeated string literals.

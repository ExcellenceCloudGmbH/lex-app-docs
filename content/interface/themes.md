---
title: Themes
---

Lex App supports two carefully crafted visual themes — **Light** and **Dark** — so you can work comfortably in any environment. Switch between them instantly using the toggle in the application header.

## Light Mode

The default experience. Clean white backgrounds with a professional Slate color palette:

- **Primary**: Teal (#14B4B4) for buttons, links, and key actions
- **Backgrounds**: White (#FFFFFF) with soft gray surfaces (#F6F8FA)
- **Accents**: Subtle separators and shadows that give depth without distraction

Light mode is ideal for well-lit offices, presentations, and daytime use. The high contrast between text and background minimizes eye strain during extended data entry sessions.

<!-- 📸 SCREENSHOT: Full grid view in light mode, showing the sidebar, toolbar, and data -->

## Dark Mode

Designed for low-light environments, late-night work, and users who simply prefer a darker interface:

- **Primary**: Teal (#14B4B4) for interactive elements
- **Backgrounds**: Deep slate tones (#0D1117, #161B22) that reduce screen glare
- **Text**: Soft white and muted gray for readability without harshness

Dark mode isn't just a color inversion — every component is individually styled. The data grid, sidebar, cards, buttons, and even the Streamlit dashboard frames are all tuned for visual consistency.

<!-- 📸 SCREENSHOT: Same grid view in dark mode -->

## How to Switch

Click the **theme toggle** icon in the application header bar, next to the search field. The switch is instant — no reload required. Your preference is remembered across sessions.

<!-- 📸 SCREENSHOT: Close-up of the header showing the theme toggle button -->

> [!tip]
> Both themes are fully compatible with all features: the [[interface/the-grid/index|data grid]], [[interface/record-detail/index|record detail tabs]], embedded [[interface/record-detail/analytics tab|Streamlit dashboards]], and [[interface/the-grid/exporting data|exported files]] all respect your chosen theme.

### Streamlit dashboards

Embedded Streamlit pages follow the Lex App theme by default, so the dashboard
and the surrounding application stay in sync. Set `LEX_THEME_FOLLOW=0` when a
dashboard needs to keep its own theme controls. While following is enabled,
Streamlit's own theme menu cannot override the mode selected in Lex App.

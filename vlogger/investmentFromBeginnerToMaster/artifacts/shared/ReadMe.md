# Ruban Investment Vlog Slide Customization Guide

This guide explains how to customize your lesson slides using shared themes, backgrounds, fonts, and special elements. All configuration and assets should be placed in the `artifacts/shared/` directory for reuse across lessons.

## 1. Theme & Style
- **ppt_theme.css**: Main theme file. Edit colors, fonts, backgrounds, and slide types here.
- **Responsive Design**: The theme is mobile-friendly and adapts to screen size. You can further adjust breakpoints in the CSS.

## 2. Backgrounds & Branding
- **background.jpg**: If present, used as the background image for all slides. The JS will automatically apply it.
- **brand.jpg**: If present, shown as the brand icon in the top-left of each slide.
- **lesson.jpg**: If present, shown as the lesson icon in the top-right or within the slide.

## 3. Configuration
- **lesson.yaml**: Place lesson-specific configuration here (e.g., title, subtitle, colors, icons). The JS will parse and apply these settings to the slides.

## 4. Custom Fonts
- Edit `ppt_theme.css` to add or change font families. You can use Google Fonts or local font files.

## 5. Special Purpose Elements
- Add images (e.g., mascot, badges) to `artifacts/shared/` and reference them in your slides or configuration.

## 6. How to Use
- Slides automatically detect and apply available assets and configuration.
- To customize:
  1. Add or replace images (background.jpg, brand.jpg, lesson.jpg) in `artifacts/shared/`.
  2. Edit `ppt_theme.css` for style changes.
  3. Edit or create `lesson.yaml` for lesson-specific settings.
  4. Use the slide type classes (`slide-primary`, `slide-info`, etc.) for different visual effects.

## 7. Example lesson.yaml
```yaml
title: "Phase 0 Lesson 1: 课程导览"
subtitle: "投资从入门到大师系列课程"
background: "background.jpg"
brand_icon: "brand.jpg"
lesson_icon: "lesson.jpg"
color_scheme: "primary"
```

## 8. Advanced Customization
- You can extend the JS (`ppt_slide.js`) to support more configuration options, transitions, or interactive elements.
- For accessibility, ensure color contrast and font size are sufficient.

## 9. Troubleshooting
- If slides are not responsive, check your CSS and ensure the theme is loaded.
- If images do not appear, verify file names and paths.
- If configuration is not applied, check the format of `lesson.yaml` and JS parsing logic.

---
For further help, see the comments in `ppt_theme.css` and `ppt_slide.js` for extension points.

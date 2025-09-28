# Task: Improve Admin Panel Design and Functionality

## Overview
Update admin templates for consistency (Tailwind CSS), fix visibility issues (black text), replace JSON inputs with structured forms, add image upload to events, improve team/contact GUIs. Update app.py for backend support.

## Steps

### 1. Update manage_home.html
- [x] Convert to Tailwind classes.
- [x] Replace features textarea with dynamic add/remove title/description inputs.
- [x] Update preview to icon-based cards (lucide icons, no photos) matching public index.html.
- [x] Ensure hero/CTA inputs have black text on light background.

### 2. Update manage_events.html
- [x] Convert to Tailwind.
- [x] Add file input for event image (enctype=multipart/form-data).
- [x] Change input text color to black.
- [x] Update event cards to display uploaded image or placeholder.

### 3. Update manage_gallery.html and gallery.html
- [x] Ensure all inputs have black text (add CSS if needed).
- [x] Add search input above filters in gallery.html with black text.
- [x] Verify hover overlays have visible white text.

### 4. Update manage_team.html
- [x] Convert to Tailwind.
- [x] Replace achievements textarea with multi-input list (add/remove).
- [x] Replace social textarea with separate URL fields (instagram, email, etc.).
- [x] Enhance core team cards: Add icons, better spacing, yellow accents.
- [x] Improve active members layout similarly.

### 5. Update manage_contact.html
- [x] Convert to Tailwind.
- [x] Add structured fields: Separate inputs for address lines, office/weekend hours.
- [x] Add individual social URL inputs (facebook, twitter, instagram, etc.).
- [x] Add dynamic FAQ section (add/remove question/answer pairs).
- [x] Replace raw lists with formatted previews.

### 6. Update static/css/style.css
- [x] Add .text-input { color: black !important; background: white; } for forms.
- [x] Fix white/blank boxes: Ensure card backgrounds are gray-800, images have fallbacks.
- [x] Add styles for dynamic forms (add/remove buttons).

### 7. Update static/js/script.js
- [x] Add functions for dynamic form fields (add/remove for features, achievements, FAQ).
- [x] Add gallery search functionality: Filter items by title/desc on input.
- [x] Ensure search input has black text.

### 8. Update app.py
- [x] Revise HomeForm: Use FieldList(FormField(FeatureForm)) for features.
- [x] Add FileField to EventForm for image; handle upload in route (save to static/images/events/).
- [x] Update TeamForm: FieldList(StringField) for achievements, separate StringFields for social keys.
- [x] Update ContactForm: Add fields for address/social/FAQ (use FieldList for FAQ).
- [x] Handle structured data parsing/saving to DB.
- [x] Add image upload logic (secure_filename, etc.).

### 9. Testing
- [ ] Run `python app.py` to start server.
- [ ] Use browser to verify each manage page: No JSON/raw text, black visible input text, image uploads work, consistent Tailwind design, no blank/white boxes.
- [ ] Check core team/contact previews are clean.

### 10. Completion
- [ ] All steps done; present final result.

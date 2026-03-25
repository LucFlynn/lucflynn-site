---
title: "How to Track Formidable Forms Conversions in Google Ads (2026 Guide)"
slug: "formidable-forms-google-ads-conversion-tracking"
description: "Step-by-step guide to tracking Formidable Forms form submissions as conversions in Google Ads. Covers GTM setup, Enhanced Conversions, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/google-ads-conversion-tracking"
page_type: "spoke"
---

# Formidable Forms + Google Ads Conversion Tracking Setup

I see this exact tracking gap in about 30% of WordPress sites running Google Ads — Formidable Forms submissions happening, but Google Ads showing zero conversions. The issue is usually that the `frmFormComplete` event isn't properly connected to Google's conversion tracking, so you're flying blind on which keywords actually drive leads.

Most setups I audit are missing Enhanced Conversions entirely, which means Google's attribution is basically useless for optimizing toward actual form fills.

## What You'll Have Working By The End

- Formidable Forms submissions automatically tracked as Google Ads conversions
- Enhanced Conversions enabled with first-party data (email, name, phone)
- Real-time conversion verification in Google Ads interface
- Proper conversion counting (One per lead, not per page view)
- Cross-platform attribution data flowing to Google's algorithm

## Prerequisites

- [ ] Google Ads account with admin access
- [ ] Google Tag Manager container installed on your WordPress site
- [ ] Formidable Forms plugin active with at least one published form
- [ ] WordPress admin access to modify form settings
- [ ] Conversion action already created in Google Ads (if not, create one under Goals → Conversions)

## Step 1: Set Up the Data Layer Event in Formidable Forms

Formidable Forms fires a JavaScript event called `frmFormComplete` when any form is submitted successfully. We need to capture this and push structured data to the data layer.

Add this code to your theme's `functions.php` file or in a custom plugin:

```php
add_action('frm_after_create_entry', 'push_formidable_to_datalayer', 30, 2);

function push_formidable_to_datalayer($entry_id, $form_id) {
    // Get the entry data
    $entry = FrmEntry::getOne($entry_id);
    $form = FrmForm::getOne($form_id);
    
    // Get field values for Enhanced Conversions
    $email = '';
    $phone = '';
    $first_name = '';
    $last_name = '';
    
    // Map common field IDs - adjust these based on your form setup
    $field_values = FrmProEntryMetaHelper::get_entry_metas($entry_id);
    
    foreach($field_values as $field) {
        $field_obj = FrmField::getOne($field->field_id);
        
        // Match by field type or field label - customize these
        if($field_obj->type == 'email') {
            $email = $field->meta_value;
        }
        if($field_obj->type == 'phone') {
            $phone = $field->meta_value;
        }
        if(stripos($field_obj->name, 'first') !== false || stripos($field_obj->name, 'fname') !== false) {
            $first_name = $field->meta_value;
        }
        if(stripos($field_obj->name, 'last') !== false || stripos($field_obj->name, 'lname') !== false) {
            $last_name = $field->meta_value;
        }
    }
    
    ?>
    <script>
    window.dataLayer = window.dataLayer || [];
    dataLayer.push({
        'event': 'formidable_form_submit',
        'form_id': '<?php echo esc_js($form_id); ?>',
        'form_name': '<?php echo esc_js($form->name); ?>',
        'entry_id': '<?php echo esc_js($entry_id); ?>',
        'enhanced_conversion_data': {
            'email': '<?php echo esc_js($email); ?>',
            'phone_number': '<?php echo esc_js($phone); ?>',
            'first_name': '<?php echo esc_js($first_name); ?>',
            'last_name': '<?php echo esc_js($last_name); ?>'
        }
    });
    </script>
    <?php
}
```

If you prefer a client-side approach (easier but slightly less reliable), add this to your site instead:

```javascript
document.addEventListener('frmFormComplete', function(event) {
    // Extract form data
    var form = event.target;
    var formId = form.querySelector('input[name="form_id"]').value;
    
    // Get Enhanced Conversions data
    var email = form.querySelector('input[type="email"]')?.value || '';
    var phone = form.querySelector('input[type="tel"]')?.value || '';
    var firstName = form.querySelector('input[name*="first"]')?.value || '';
    var lastName = form.querySelector('input[name*="last"]')?.value || '';
    
    window.dataLayer = window.dataLayer || [];
    dataLayer.push({
        'event': 'formidable_form_submit',
        'form_id': formId,
        'enhanced_conversion_data': {
            'email': email,
            'phone_number': phone,
            'first_name': firstName,
            'last_name': lastName
        }
    });
});
```

## Step 2: Create the GTM Trigger

In Google Tag Manager:

1. Go to **Triggers** → **New**
2. Name it "Formidable Forms - All Submissions"
3. Trigger Type: **Custom Event**
4. Event name: `formidable_form_submit`
5. Leave "This trigger fires on" set to "All Custom Events"

If you want to track specific forms only:
1. Select "Some Custom Events"
2. Add condition: `form_id` `equals` `[your form ID]`

## Step 3: Create Data Layer Variables

Create these variables in GTM to access the Enhanced Conversions data:

**Variable 1: Enhanced Conversion Email**
- Name: "EC - Email"
- Type: Data Layer Variable
- Data Layer Variable Name: `enhanced_conversion_data.email`

**Variable 2: Enhanced Conversion Phone**
- Name: "EC - Phone"  
- Type: Data Layer Variable
- Data Layer Variable Name: `enhanced_conversion_data.phone_number`

**Variable 3: Enhanced Conversion First Name**
- Name: "EC - First Name"
- Type: Data Layer Variable  
- Data Layer Variable Name: `enhanced_conversion_data.first_name`

**Variable 4: Enhanced Conversion Last Name**
- Name: "EC - Last Name"
- Type: Data Layer Variable
- Data Layer Variable Name: `enhanced_conversion_data.last_name`

## Step 4: Configure the Google Ads Conversion Tag

1. In GTM, go to **Tags** → **New**
2. Name: "Google Ads - Formidable Forms Conversion"
3. Tag Type: **Google Ads Conversion Tracking**
4. Configuration:
   - **Conversion ID**: Your Google Ads conversion ID (format: AW-XXXXXXXXXX)
   - **Conversion Label**: Your specific conversion label
   - **Conversion Value**: Leave blank or set static value if all leads have same value
   - **Order ID**: `{{DLV - Entry ID}}` (prevents duplicate counting)
   - **Currency Code**: USD (or your currency)

5. **Enhanced Conversions Settings**:
   - Check "Enable Enhanced Conversions"
   - User-provided data source: "Code"
   - Email: `{{EC - Email}}`
   - Phone: `{{EC - Phone}}`  
   - First Name: `{{EC - First Name}}`
   - Last Name: `{{EC - Last Name}}`

6. **Triggering**: Select your "Formidable Forms - All Submissions" trigger

## Step 5: Set Up Conversion Action Settings in Google Ads

In your Google Ads account:

1. Go to **Goals** → **Conversions**
2. Find your conversion action and click to edit
3. Set **Count**: "One" (crucial for lead gen)
4. Set **Attribution model**: "Position-based" or "Time decay" 
5. **Conversion window**: 30 days (default) or adjust based on your sales cycle
6. **View-through window**: 1 day for most B2B, 7 days for B2C

## Testing & Verification

**Test the data layer push:**
1. Open Chrome DevTools → Console
2. Submit a test form
3. Type: `dataLayer`
4. Verify you see an object with `event: 'formidable_form_submit'` and all your enhanced conversion data

**Test in GTM Preview Mode:**
1. Enable Preview mode in GTM
2. Submit your form
3. Look for the `formidable_form_submit` event in the Summary
4. Verify your Google Ads tag fired
5. Check that all Enhanced Conversions variables populated with real data

**Verify in Google Ads:**
1. Go to **Goals** → **Conversions**
2. Look for a green dot in the "Status" column within 24 hours
3. Check the "Conversions" column for count increases
4. For Enhanced Conversions, look for the enhanced conversion rate % (should be 60-90% if data quality is good)

**Cross-check the numbers:**
- Formidable Forms entries (WordPress admin → Formidable → Entries)
- Google Ads conversions (last 7 days)
- Acceptable variance: 5-15% (some users block tags, some submit multiple times)

## Troubleshooting

**Problem: GTM tag firing but no conversions in Google Ads**
Check your Conversion ID format — it should be exactly `AW-XXXXXXXXXX`, not just the numeric part. Also verify the conversion label matches exactly (case sensitive).

**Problem: Enhanced Conversions showing 0% match rate**
Your field mapping is probably wrong. Go back to your data layer code and `console.log()` each field to see what's actually being captured. Most commonly, people map field IDs instead of field values.

**Problem: Duplicate conversions for single form submission**
You're missing the Order ID or it's not unique. Use the Formidable entry ID as the Order ID — it's automatically unique per submission.

**Problem: Conversions tracking but attribution is wonky**
Check your conversion window settings. If you're seeing conversions attributed to "Direct" that should be paid search, your window might be too short for your customer journey.

**Problem: Data layer event not firing on form submit**
The `frmFormComplete` event only fires after successful validation. If you're testing with invalid data (missing required fields), the event won't trigger. Also check that you're not preventing the default form behavior in other JavaScript.

**Problem: Some forms tracking, others not**
Different Formidable forms might have different field structures. Check that your field mapping logic (especially the `stripos` searches) matches the actual field names across all your forms.

## What To Do Next

Once your Formidable Forms → Google Ads tracking is working, consider these related setups:

- [Formidable Forms Meta Ads Conversion Tracking](/tracking/formidable-forms-meta-ads-conversion-tracking) — Get the same data into Facebook
- [Formidable Forms GA4 Conversion Tracking](/tracking/formidable-forms-ga4-conversion-tracking) — Complete your analytics picture  
- [Formidable Forms LinkedIn Ads Conversion Tracking](/tracking/formidable-forms-linkedin-ads-conversion-tracking) — B2B attribution
- [Formidable Forms to HubSpot Integration](/integrations/formidable-forms-to-hubspot) — Get these leads into your CRM automatically

Need help getting this set up? [Get a free tracking audit](/contact) — I'll review your current setup and show you exactly what's missing.

*This guide is part of the [Google Ads Conversion Tracking Hub](/tracking/google-ads-conversion-tracking) — complete guides for tracking any conversion source in Google Ads.*
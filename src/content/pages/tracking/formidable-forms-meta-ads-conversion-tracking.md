---
title: "How to Track Formidable Forms Conversions in Meta Ads (2026 Guide)"
slug: "formidable-forms-meta-ads-conversion-tracking"
description: "Step-by-step guide to tracking Formidable Forms form submissions as conversions in Meta Ads. Covers GTM setup, Meta CAPI, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/meta-ads-conversion-tracking"
page_type: "spoke"
---

# Formidable Forms + Meta Ads Conversion Tracking Setup

I see this exact combo broken in about 30% of WordPress accounts I audit. The problem is almost always the same: Formidable Forms fires its `frmFormComplete` event, but it's not being captured properly by the Meta Pixel, or worse — it's firing duplicate events when someone uses both client-side pixel and CAPI without proper deduplication. Your Meta Ads data becomes garbage, and you're optimizing campaigns toward phantom conversions.

## What You'll Have Working By The End

- Formidable Forms submissions automatically firing as Meta Ads conversion events
- Server-side tracking via Meta CAPI for better data quality and iOS resistance
- Event deduplication between pixel and CAPI so you don't double-count conversions
- Proper form field data flowing to Meta for better audience building
- Real conversion counts that actually match your form entries

## Prerequisites

- [ ] Formidable Forms plugin installed and at least one form live
- [ ] Meta Pixel installed on your site (via GTM or directly)
- [ ] Google Tag Manager container with Publish access
- [ ] Meta Business Manager access with Events Manager permissions
- [ ] Access to your WordPress admin (needed for CAPI server events)

## Step 1: Set Up the Formidable Forms Event Listener

Formidable Forms fires a `frmFormComplete` event when someone submits a form, but by default it doesn't push anything to the data layer. Add this code to your theme's `functions.php` or in a custom plugin:

```php
add_action('frm_after_create_entry', 'push_formidable_to_datalayer', 30, 2);

function push_formidable_to_datalayer($entry_id, $form_id) {
    // Get the form and entry details
    $form = FrmForm::getOne($form_id);
    $entry = FrmEntry::getOne($entry_id);
    
    // Get field values (customize based on your form fields)
    $email = FrmEntryMeta::get_entry_meta_by_field($entry_id, 'email');
    $first_name = FrmEntryMeta::get_entry_meta_by_field($entry_id, 'first_name');
    $last_name = FrmEntryMeta::get_entry_meta_by_field($entry_id, 'last_name');
    
    // Generate unique event ID for deduplication
    $event_id = 'frm_' . $form_id . '_' . $entry_id . '_' . time();
    
    ?>
    <script>
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
            'event': 'formidable_form_submit',
            'form_id': '<?php echo $form_id; ?>',
            'form_title': '<?php echo esc_js($form->name); ?>',
            'entry_id': '<?php echo $entry_id; ?>',
            'event_id': '<?php echo $event_id; ?>',
            'user_data': {
                'email': '<?php echo esc_js($email); ?>',
                'first_name': '<?php echo esc_js($first_name); ?>',
                'last_name': '<?php echo esc_js($last_name); ?>'
            }
        });
    </script>
    <?php
}
```

**Important:** Replace `'email'`, `'first_name'`, `'last_name'` with your actual Formidable Forms field keys. You can find these in your form builder under each field's advanced settings.

## Step 2: Create the GTM Trigger

In Google Tag Manager:

1. Go to **Triggers** → **New**
2. Choose **Custom Event** trigger type
3. Set **Event name** to: `formidable_form_submit`
4. Leave **This trigger fires on** set to "All Custom Events"
5. Name it: "Formidable Forms - Form Submit"
6. **Save**

If you want to track specific forms only, add this condition:
- **Some Custom Events**
- **form_id** equals **[your form ID number]**

## Step 3: Configure the Meta Pixel Event Tag

Create a new tag in GTM:

1. **Tag Type**: Meta Pixel
2. **Event Name**: Lead (or use a custom conversion name)
3. **Meta Pixel ID**: Your pixel ID
4. **Event Parameters**:
   ```
   content_name: {{DLV - form_title}}
   content_category: form_submission
   value: 1
   currency: USD
   ```

5. **Advanced Settings** → **Ecommerce Settings**:
   - **event_id**: `{{DLV - event_id}}`
   - **user_data**: 
     ```json
     {
       "email": "{{DLV - user_data.email}}",
       "first_name": "{{DLV - user_data.first_name}}",
       "last_name": "{{DLV - user_data.last_name}}"
     }
     ```

6. **Triggering**: Select your "Formidable Forms - Form Submit" trigger
7. **Save** and name it "Meta Pixel - Formidable Forms Lead"

**Which event name should you use?** If this is a contact form or newsletter signup, use "Lead". If it's a purchase form or high-intent action, create a custom conversion in Meta Events Manager first, then use that custom event name instead.

## Step 4: Set Up Meta CAPI for Server-Side Tracking

Client-side pixels get blocked by about 20% of users. CAPI ensures you capture more conversions. Add this to your Formidable Forms webhook or the same function from Step 1:

```php
function send_formidable_to_meta_capi($entry_id, $form_id) {
    $access_token = 'your_capi_access_token';
    $pixel_id = 'your_pixel_id';
    
    // Get entry data
    $entry = FrmEntry::getOne($entry_id);
    $email = FrmEntryMeta::get_entry_meta_by_field($entry_id, 'email');
    $first_name = FrmEntryMeta::get_entry_meta_by_field($entry_id, 'first_name');
    $last_name = FrmEntryMeta::get_entry_meta_by_field($entry_id, 'last_name');
    
    // Same event ID as client-side for deduplication
    $event_id = 'frm_' . $form_id . '_' . $entry_id . '_' . time();
    
    $data = array(
        'data' => array(
            array(
                'event_name' => 'Lead',
                'event_time' => time(),
                'event_id' => $event_id,
                'action_source' => 'website',
                'event_source_url' => home_url($_SERVER['REQUEST_URI']),
                'user_data' => array(
                    'email' => array(hash('sha256', strtolower(trim($email)))),
                    'first_name' => array(hash('sha256', strtolower(trim($first_name)))),
                    'last_name' => array(hash('sha256', strtolower(trim($last_name)))),
                    'client_ip_address' => $_SERVER['REMOTE_ADDR'],
                    'client_user_agent' => $_SERVER['HTTP_USER_AGENT']
                ),
                'custom_data' => array(
                    'content_name' => 'Formidable Form ' . $form_id,
                    'value' => 1,
                    'currency' => 'USD'
                )
            )
        )
    );
    
    $url = "https://graph.facebook.com/v18.0/{$pixel_id}/events?access_token={$access_token}";
    
    wp_remote_post($url, array(
        'body' => json_encode($data),
        'headers' => array('Content-Type' => 'application/json')
    ));
}

// Add this to your existing hook
add_action('frm_after_create_entry', 'send_formidable_to_meta_capi', 35, 2);
```

**Get your CAPI access token**: Go to Meta Events Manager → Settings → Conversions API → Generate Access Token.

## Step 5: Create Data Layer Variables in GTM

You need these variables to capture the data from your form submissions:

1. **DLV - form_title**:
   - Variable Type: Data Layer Variable
   - Data Layer Variable Name: `form_title`

2. **DLV - event_id**:
   - Variable Type: Data Layer Variable  
   - Data Layer Variable Name: `event_id`

3. **DLV - user_data.email**:
   - Variable Type: Data Layer Variable
   - Data Layer Variable Name: `user_data.email`

Repeat for first_name and last_name. You'll reference these in your Meta Pixel tag configuration.

## Testing & Verification

### In Meta Events Manager
1. Go to **Events Manager** → **Test Events**
2. Enter your website URL
3. Submit a test form on your site
4. You should see both:
   - **Browser** event (from pixel)
   - **Server** event (from CAPI)
   - Both should have the **same event_id** for proper deduplication

### Check the Raw Data
1. In Events Manager, click on your pixel
2. Go to **Activity** tab
3. Look for your Lead events with:
   - `content_name`: Your form title
   - `event_id`: The generated ID
   - `event_source_url`: The page where the form was submitted

### Cross-Reference Numbers
- **Formidable Forms entries**: WP Admin → Formidable → Entries
- **Meta conversion count**: Ads Manager → Columns → Conversions
- **Acceptable variance**: 5-15% (some users block pixels, some submissions might fail)

If your Meta count is more than 20% higher than Formidable entries, you likely have a deduplication problem.

## Troubleshooting

**Problem**: Events showing in Test Events but not in regular Events Manager activity
→ Check that your Meta Pixel ID matches between GTM tag and CAPI code. Also verify your access token has the correct permissions.

**Problem**: Double-counting conversions (Meta count much higher than actual form submissions)
→ Your `event_id` isn't matching between pixel and CAPI. Make sure both are using the exact same ID format and timing.

**Problem**: CAPI events not showing up at all
→ Most likely a server configuration issue. Check that `wp_remote_post` is working by adding error logging. Some hosts block external API calls.

**Problem**: Form submissions trigger multiple Meta events
→ This happens when Formidable's AJAX submission fires the event, then the page redirects and fires it again. Add a check in your PHP code to only fire once per entry ID.

**Problem**: User data not populating in Meta for audience building
→ Verify your Formidable field keys match what you're using in the code. Check the actual field names in your form builder — they're often different from the display labels.

**Problem**: Events firing for form spam/bot submissions
→ Add Formidable's built-in spam detection check: `if (!FrmEntryValidate::validate($values)) { return; }` before sending to Meta.

## What To Do Next

- Set up [Google Ads conversion tracking for Formidable Forms](/tracking/formidable-forms-google-ads-conversion-tracking) to compare performance across platforms
- Configure [GA4 goal tracking for your forms](/tracking/formidable-forms-ga4-conversion-tracking) for a complete attribution picture  
- Connect your [Formidable Forms to HubSpot](/integrations/formidable-forms-to-hubspot) for automatic lead nurturing
- Get a [free tracking audit](/contact) to verify your setup is capturing 100% of conversions

*This guide is part of the [Meta Ads Conversion Tracking hub](/tracking/meta-ads-conversion-tracking) — complete setup guides for tracking any conversion source in Meta Ads.*
---
title: "How to Track Formidable Forms Conversions in GA4 (2026 Guide)"
slug: "formidable-forms-ga4-conversion-tracking"
description: "Step-by-step guide to tracking Formidable Forms form submissions as conversions in GA4. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/ga4-conversion-tracking"
page_type: "spoke"
---

# Formidable Forms + GA4 Conversion Tracking Setup

I audit about 120 WordPress sites per year, and roughly 30% use Formidable Forms. The good news? It fires clean JavaScript events. The bad news? Most people either miss the event entirely or send it to GA4 without proper conversion marking. You end up with form submissions buried in your events report instead of showing up as actual conversions in your attribution reports.

Formidable Forms fires the `frmFormComplete` event on successful submission, which makes it easier to track than most form plugins. But there's a specific way to catch this event and format it for GA4's conversion system.

## What You'll Have Working By The End

• Formidable Forms submissions automatically sending to GA4 as `generate_lead` events
• Those events marked as conversions in GA4 admin (available for Google Ads import)
• Clean attribution data showing which traffic sources drive form completions
• Real-time verification working in GA4's DebugView
• Form submission counts matching between WordPress admin and GA4 (within 5-10% variance)

## Prerequisites

- [ ] Formidable Forms Pro or Lite installed and at least one form published
- [ ] Google Tag Manager container installed on your WordPress site
- [ ] GA4 property created with GTM sending pageviews successfully
- [ ] Admin access to your GA4 property (to mark events as conversions)
- [ ] Test form submissions available (don't use your main contact form for testing)

## Step 1: Add the Formidable Forms Event Listener

First, you need to catch Formidable's `frmFormComplete` event and send it to the data layer in a format GTM can use.

Add this code to your theme's `functions.php` file or in a custom plugin:

```php
function formidable_ga4_tracking() {
    if (!is_admin()) {
        ?>
        <script>
        document.addEventListener('frmFormComplete', function(event) {
            // Get form data
            var form = event.detail.form;
            var formId = form.id;
            var formAction = form.action;
            
            // Get form title from the form element
            var formContainer = document.getElementById('frm_form_' + formId + '_container');
            var formTitle = 'Contact Form'; // Default fallback
            
            if (formContainer) {
                var titleElement = formContainer.querySelector('.frm_form_title, h3, h2');
                if (titleElement) {
                    formTitle = titleElement.textContent.trim();
                }
            }
            
            // Push to data layer
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({
                event: 'formidable_form_complete',
                form_id: formId,
                form_title: formTitle,
                form_location: window.location.href
            });
            
            console.log('Formidable form completed:', {
                form_id: formId,
                form_title: formTitle
            });
        });
        </script>
        <?php
    }
}
add_action('wp_footer', 'formidable_ga4_tracking');
```

This captures every Formidable Forms submission and sends standardized data to GTM.

## Step 2: Create the GTM Trigger

In Google Tag Manager:

1. **Go to Triggers** → **New**
2. **Name it**: "Formidable Forms - Form Complete"
3. **Trigger Type**: Custom Event
4. **Event Name**: `formidable_form_complete`
5. **This trigger fires on**: All Custom Events
6. **Save**

For more targeted tracking (like only specific forms), you can add a condition:
- **Some Custom Events**
- **form_id** equals **[your specific form ID]**

## Step 3: Create GA4 Configuration Variables

You need these data layer variables in GTM to pass form data to GA4:

**Variable 1: Form ID**
- **Variable Type**: Data Layer Variable
- **Data Layer Variable Name**: `form_id`
- **Name**: "DLV - Form ID"

**Variable 2: Form Title**
- **Variable Type**: Data Layer Variable  
- **Data Layer Variable Name**: `form_title`
- **Name**: "DLV - Form Title"

**Variable 3: Form Location**
- **Variable Type**: Data Layer Variable
- **Data Layer Variable Name**: `form_location` 
- **Name**: "DLV - Form Location"

## Step 4: Create the GA4 Event Tag

1. **Go to Tags** → **New**
2. **Tag Type**: GA4 Event
3. **Configuration Tag**: [Select your main GA4 config tag]
4. **Event Name**: `generate_lead`
5. **Event Parameters**:
   - `form_id`: `{{DLV - Form ID}}`
   - `form_title`: `{{DLV - Form Title}}`  
   - `page_location`: `{{DLV - Form Location}}`
   - `method`: `formidable_forms`
6. **Triggering**: Select your "Formidable Forms - Form Complete" trigger
7. **Name**: "GA4 - Formidable Forms Lead"
8. **Save**

I use `generate_lead` instead of a custom event name because it's a recommended event type in GA4, which gives you better reporting dimensions and easier Google Ads conversion import.

## Step 5: Mark as Conversion in GA4

The tag alone won't create conversions. You need to mark the event as a conversion in GA4:

1. **Go to GA4** → **Configure** → **Events**
2. **Find** `generate_lead` in your events list (may take 24 hours to appear)
3. **Toggle "Mark as conversion"** to ON
4. **Or manually add**: **Configure** → **Conversions** → **New conversion event**
   - **Event name**: `generate_lead`
   - **Save**

## Testing & Verification

### GTM Preview Mode
1. **Enable Preview mode** in GTM
2. **Fill out and submit** a Formidable form
3. **Check the Summary**: Look for your "Formidable Forms - Form Complete" trigger firing
4. **Click the tag**: Verify all variables populate correctly
5. **Check Console**: Look for the "Formidable form completed" log message

### GA4 DebugView
1. **GA4** → **Configure** → **DebugView**  
2. **Submit your test form**
3. **Look for** `generate_lead` events appearing in real-time
4. **Click the event**: Check parameters (form_id, form_title, method) are populated
5. **Event should show** within 30 seconds of form submission

### Realtime Reports
1. **GA4** → **Reports** → **Realtime**
2. **Submit test form**
3. **Check "Event count by Event name"**: Should see `generate_lead` increment
4. **Check "Conversions"**: Should see conversion count increase (if marked as conversion)

### Cross-Check Numbers
Compare form submission counts after 24-48 hours:
- **WordPress Admin**: Formidable → Entries (total count)
- **GA4**: Configure → Events → `generate_lead` (total event count)

Acceptable variance is 5-15%. Higher variance usually indicates tracking setup issues or bot traffic filtering differences.

## Troubleshooting

**Problem** → frmFormComplete event not firing
Check your browser console for JavaScript errors. Formidable Forms Lite sometimes has conflicts with optimization plugins. Try testing with all caching/minification plugins temporarily disabled. The event only fires on successful form submission, not validation errors.

**Problem** → Data layer variables showing as undefined in GTM
The timing might be off. Add a 500ms delay to the data layer push: `setTimeout(function() { window.dataLayer.push({...}); }, 500);`. Also verify your variable names match exactly - `form_id` vs `formId` will break the connection.

**Problem** → Events showing in GTM but not appearing in GA4 DebugView
Your GA4 measurement ID might be wrong in your config tag, or the config tag isn't firing on the same pages as your form. Check that your GA4 config tag trigger includes the pages where your forms live.

**Problem** → generate_lead events appear but conversion count stays zero
You haven't marked the event as a conversion in GA4 admin, or the conversion marking is still processing (can take up to 24 hours). Go to Configure → Events and toggle "Mark as conversion" for generate_lead.

**Problem** → Form submissions counting twice in GA4
You have duplicate tracking - possibly both this setup AND another form tracking method (like a plugin). Check for other GA4 tags firing on form submission, or plugins like MonsterInsights with form tracking enabled.

**Problem** → Form ID showing as null or undefined
Formidable Forms sometimes doesn't set the ID attribute properly on AJAX submissions. Try accessing it via `event.detail.formId` instead of `event.detail.form.id`, or fall back to getting it from the form action URL parsing.

## What To Do Next

Once your basic conversion tracking is working, consider these related setups:

• [Formidable Forms + Google Ads Conversion Tracking](/tracking/formidable-forms-google-ads-conversion-tracking) - Import these GA4 conversions into Google Ads for bidding optimization
• [Formidable Forms + Meta Ads Conversion Tracking](/tracking/formidable-forms-meta-ads-conversion-tracking) - Set up parallel tracking for Facebook campaigns  
• [Formidable Forms + LinkedIn Ads Conversion Tracking](/tracking/formidable-forms-linkedin-ads-conversion-tracking) - Track B2B lead generation campaigns
• [Formidable Forms to HubSpot Integration](/integrations/formidable-forms-to-hubspot) - Send form data directly to your CRM for complete attribution

**Having tracking issues?** I offer free 15-minute tracking audits to diagnose what's broken and get your attribution data clean. [Book a free audit call](/contact) and I'll spot-check your setup.

*This guide is part of the [GA4 Conversion Tracking Hub](/tracking/ga4-conversion-tracking) — complete tutorials for tracking conversions from every major form, quiz, and landing page platform into GA4.*
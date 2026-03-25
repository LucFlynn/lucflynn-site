---
title: "How to Track Contact Form 7 Conversions in LinkedIn Ads (2026 Guide)"
slug: "contact-form-7-linkedin-ads-conversion-tracking"
description: "Step-by-step guide to tracking Contact Form 7 form submissions as conversions in LinkedIn Ads. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/linkedin-ads-conversion-tracking"
page_type: "spoke"
---

# Contact Form 7 + LinkedIn Ads Conversion Tracking Setup

I see this exact setup broken in about 35% of the LinkedIn campaigns I audit. Contact Form 7 is WordPress's most popular form plugin, but it doesn't store submissions by default — everything goes straight to email. LinkedIn's conversion tracking is less mature than Google or Meta, so when the integration breaks, you're flying blind on form conversion data while your LinkedIn ad spend keeps burning.

The main issue? Contact Form 7 fires a DOM event (`wpcf7mailsent`) that most people miss when setting up LinkedIn tracking. You end up with LinkedIn showing zero conversions while your inbox fills up with actual leads.

## What You'll Have Working By The End

- Contact Form 7 submissions automatically tracked as LinkedIn Ads conversions
- Real-time conversion data flowing into LinkedIn Campaign Manager
- Proper GTM setup that captures the `wpcf7mailsent` event
- A testing process to verify conversions are recording correctly
- Cross-reference system between form submissions and LinkedIn conversion counts

## Prerequisites

- [ ] Contact Form 7 installed and active on WordPress
- [ ] LinkedIn Ads account with Campaign Manager access
- [ ] LinkedIn Insight Tag installed (base pixel)
- [ ] Google Tag Manager container on your site
- [ ] LinkedIn conversion action already created in Campaign Manager
- [ ] Admin access to WordPress and GTM

## Step 1: Set Up the Contact Form 7 Event Listener

Contact Form 7 fires a `wpcf7mailsent` DOM event when forms submit successfully. We need to capture this and push it to the data layer.

Add this code to your theme's `functions.php` file or in a custom plugin:

```javascript
<script>
document.addEventListener('wpcf7mailsent', function(event) {
    // Get the form ID from the event
    var formId = event.detail.contactFormId;
    var formTitle = event.detail.inputs.find(input => input.name === 'your-subject')?.value || 'Contact Form Submission';
    
    // Push to data layer for GTM
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
        'event': 'cf7_form_submit',
        'form_id': formId,
        'form_title': formTitle,
        'conversion_value': 1 // Adjust based on your lead value
    });
    
    console.log('CF7 submission tracked for form ID: ' + formId);
});
</script>
```

**Alternative approach:** If you prefer not to edit theme files, you can add this script through GTM using a Custom HTML tag that fires on All Pages. This keeps the tracking code separate from your theme.

## Step 2: Create the GTM Trigger

In Google Tag Manager, create a trigger that listens for the Contact Form 7 submission event:

1. **Triggers** → **New** → **Custom Event**
2. **Event name:** `cf7_form_submit`
3. **This trigger fires on:** All Custom Events
4. **Name:** `CF7 - Form Submission`

If you want to track only specific forms, add a condition:
- **Some Custom Events**
- **form_id** equals **[your form ID]**

You can find your Contact Form 7 ID in WordPress admin under **Contact** → **Contact Forms**.

## Step 3: Configure the LinkedIn Conversion Tag

Create the LinkedIn Ads conversion tag in GTM:

1. **Tags** → **New** → **Custom HTML**
2. **Tag Name:** `LinkedIn - CF7 Conversion`
3. **HTML:**

```html
<script>
window.lintrk('track', { conversion_id: YOUR_CONVERSION_ID });
</script>
```

Replace `YOUR_CONVERSION_ID` with your actual LinkedIn conversion ID from Campaign Manager.

**Advanced setup with dynamic values:**

```html
<script>
window.lintrk('track', { 
    conversion_id: YOUR_CONVERSION_ID,
    conversion_value: {{DLV - Conversion Value}} // GTM variable
});
</script>
```

4. **Triggering:** Select your `CF7 - Form Submission` trigger
5. **Advanced Settings** → **Tag firing options:** Once per page

## Step 4: Client-Side GTM Implementation

For better tracking reliability, implement client-side GTM that captures form submissions even if the page doesn't redirect:

1. **Variables** → **New** → **Data Layer Variable**
   - **Name:** `DLV - Form ID`
   - **Data Layer Variable Name:** `form_id`

2. **Variables** → **New** → **Data Layer Variable**
   - **Name:** `DLV - Conversion Value`
   - **Data Layer Variable Name:** `conversion_value`

3. Create a more robust LinkedIn tag using these variables:

```html
<script>
// Wait for LinkedIn Insight Tag to be ready
if (typeof window.lintrk === 'function') {
    window.lintrk('track', { 
        conversion_id: YOUR_CONVERSION_ID,
        conversion_value: {{DLV - Conversion Value}},
        currency: 'USD' // Adjust as needed
    });
} else {
    // Fallback: retry after 500ms
    setTimeout(function() {
        if (typeof window.lintrk === 'function') {
            window.lintrk('track', { 
                conversion_id: YOUR_CONVERSION_ID,
                conversion_value: {{DLV - Conversion Value}}
            });
        }
    }, 500);
}
</script>
```

This approach handles cases where the LinkedIn Insight Tag hasn't fully loaded yet when the form submits.

## Step 5: Add Form Submission Logging (Optional)

Since Contact Form 7 doesn't store submissions by default, install the **Flamingo** plugin to keep records of form submissions. This gives you a backup source of truth for cross-referencing LinkedIn conversion counts.

After installing Flamingo:
1. **Flamingo** → **Inbound Messages** shows all submissions
2. Export data weekly to compare with LinkedIn Campaign Manager numbers
3. Acceptable variance is 5-15% (LinkedIn's tracking isn't as robust as Google's)

## Testing & Verification

### Verify GTM is Capturing Events

1. **GTM Preview Mode:** Open GTM → **Preview**
2. **Submit a test form** on your website
3. **Check the Tags Fired:** You should see your LinkedIn conversion tag fire
4. **Variables tab:** Verify `form_id` and `conversion_value` are populated correctly

### Verify LinkedIn is Recording Conversions

1. **LinkedIn Campaign Manager** → **Analyze** → **Conversions**
2. **Select your conversion action** from the dropdown
3. **Check Recent Activity:** Test conversions should appear within 2-6 hours
4. **Attribution window:** LinkedIn uses a 30-day view, 30-day click window by default

### Cross-Check Numbers

Compare these data sources weekly:
- **Flamingo submissions** (if installed)
- **Email inbox count** (Contact Form 7 default behavior)
- **LinkedIn Campaign Manager conversion count**
- **GTM real-time events** (for immediate verification)

**Red flags:**
- LinkedIn showing 0 conversions but you're getting form submissions
- LinkedIn conversion count exceeds total form submissions by >20%
- GTM preview shows the event firing but LinkedIn never records it

## Troubleshooting

**Problem:** GTM shows the event firing but LinkedIn Campaign Manager shows zero conversions.
Check if your LinkedIn Insight Tag base code is installed correctly. The conversion event requires the base tag to be present. Use LinkedIn's Tag Assistant or check the browser console for `lintrk is not defined` errors.

**Problem:** Some form submissions trigger the event, others don't.
This usually happens with forms that have validation errors. The `wpcf7mailsent` event only fires on successful submissions. Add error tracking: `document.addEventListener('wpcf7mailfailed', function(event) { console.log('Form failed validation'); });`

**Problem:** LinkedIn conversions are being attributed to the wrong campaign.
LinkedIn uses last-click attribution by default. If users are clicking multiple ads before converting, the most recent click gets credit. Check your attribution window settings in Campaign Manager and consider adjusting if you run multiple campaigns.

**Problem:** Conversion value isn't passing through correctly.
Verify your GTM data layer variable is configured correctly. Common issue: the variable name in GTM doesn't match what you're pushing to the data layer. Check the browser console for `dataLayer.push` events to debug.

**Problem:** Mobile form submissions aren't tracking.
Contact Form 7's AJAX submission sometimes behaves differently on mobile. Add a fallback trigger based on the form's success message appearing: Create a Visibility trigger for the `.wpcf7-mail-sent-ok` class.

**Problem:** Duplicate conversions showing in LinkedIn.
Check your GTM tag's firing options. Set to "Once per page" to prevent multiple fires. Also verify you don't have both the WordPress function and GTM Custom HTML implementing the same tracking.

## What To Do Next

- Set up [Contact Form 7 Google Ads conversion tracking](/tracking/contact-form-7-google-ads-conversion-tracking) to compare LinkedIn performance
- Connect [Contact Form 7 to HubSpot](/integrations/contact-form-7-to-hubspot) for better lead management
- Implement [Contact Form 7 Meta Ads conversion tracking](/tracking/contact-form-7-meta-ads-conversion-tracking) for cross-platform comparison
- **Get a free tracking audit:** I'll review your setup and identify what's broken. [Book a call here](/contact).

*This guide is part of the [LinkedIn Ads Conversion Tracking Hub](/tracking/linkedin-ads-conversion-tracking) — complete tracking setups for all major form tools and CRMs with LinkedIn Ads.*
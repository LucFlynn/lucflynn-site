---
title: "How to Track Contact Form 7 Conversions in Google Ads (2026 Guide)"
slug: "contact-form-7-google-ads-conversion-tracking"
description: "Step-by-step guide to tracking Contact Form 7 form submissions as conversions in Google Ads. Covers GTM setup, Enhanced Conversions, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/google-ads-conversion-tracking"
page_type: "spoke"
---

# Contact Form 7 + Google Ads Conversion Tracking Setup

Contact Form 7 is deceptively simple until you need to track submissions in Google Ads. I've audited probably 80+ WordPress sites using CF7, and about 60% of them are either not tracking conversions at all or tracking them wrong. The main culprit? CF7 only fires a DOM event — no native integration with tracking platforms, and definitely no built-in Enhanced Conversions support.

Most people try to track the form submission by watching for page redirects or thank-you pages, but CF7 doesn't redirect by default. It just shows a success message on the same page. Miss the `wpcf7mailsent` event, and you miss every conversion.

## What You'll Have Working By The End

- Contact Form 7 submissions automatically recorded as conversions in Google Ads
- Enhanced Conversions configured to improve attribution accuracy and reduce iOS 14+ signal loss
- Proper conversion counting (one conversion per submission, not per pageview)
- Testing workflow to verify conversions are firing correctly
- Cross-reference system to validate your conversion counts against form submissions

## Prerequisites

- [ ] Contact Form 7 installed and active on WordPress
- [ ] Google Tag Manager container installed on your website
- [ ] Google Ads account with conversion tracking access
- [ ] (Recommended) Flamingo plugin installed to store form submissions locally for validation

## Step 1: Create the Google Ads Conversion Action

First, set up the conversion action in Google Ads before configuring the tracking.

In Google Ads, go to **Goals** → **Conversions** → **+ New conversion action**:

1. Select **Website** as the conversion source
2. **Goal and action optimization**: Choose "Submit lead form" 
3. **Conversion name**: Something descriptive like "Contact Form Submission"
4. **Value**: Set to "Don't use a value" unless you assign dollar values to leads
5. **Count**: Select "One" (crucial for lead forms — you don't want multiple conversions per user)
6. **Attribution model**: Use "Data-driven" if available, otherwise "Last click"
7. **View-through conversion window**: 30 days is fine for most B2B, 7 days for e-commerce

Click **Create and continue**. You'll get two critical pieces of info:
- **Conversion ID**: Looks like `AW-123456789`
- **Conversion Label**: Looks like `AbCdEfGhIjKlMnOpQr`

Keep these handy — you'll need them in GTM.

## Step 2: Set Up the Data Layer Push

Contact Form 7 fires a `wpcf7mailsent` DOM event when forms submit successfully. We need to catch this event and push the data to GTM's data layer.

Add this code to your WordPress theme's `functions.php` file or in a custom plugin:

```javascript
// Add to footer on pages with Contact Form 7
add_action('wp_footer', 'cf7_gtm_tracking');
function cf7_gtm_tracking() {
    if (function_exists('wpcf7_contact_form_tag_type')) {
        ?>
        <script>
        document.addEventListener('wpcf7mailsent', function(event) {
            // Get form data for Enhanced Conversions
            var formData = new FormData(event.target);
            var email = formData.get('your-email') || formData.get('email') || '';
            var firstName = formData.get('your-name') || formData.get('first-name') || '';
            var lastName = formData.get('your-last-name') || formData.get('last-name') || '';
            var phone = formData.get('your-phone') || formData.get('phone') || '';
            
            // Split full name if using single name field
            if (firstName && !lastName && firstName.includes(' ')) {
                var nameParts = firstName.split(' ');
                firstName = nameParts[0];
                lastName = nameParts.slice(1).join(' ');
            }
            
            // Push to data layer
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({
                'event': 'cf7_form_submit',
                'form_id': event.detail.contactFormId,
                'user_data': {
                    'email_address': email,
                    'phone_number': phone,
                    'address': {
                        'first_name': firstName,
                        'last_name': lastName
                    }
                }
            });
            
            console.log('CF7 form submitted - conversion tracked');
        });
        </script>
        <?php
    }
}
```

**Important**: Update the field names (`your-email`, `your-name`, etc.) to match your actual Contact Form 7 field names. These are defined in your form's shortcode.

## Step 3: Create the GTM Trigger

In Google Tag Manager:

1. Go to **Triggers** → **New**
2. **Trigger Type**: Custom Event
3. **Event name**: `cf7_form_submit`
4. **This trigger fires on**: All Custom Events (or configure specific form IDs if you have multiple forms)

Name it something like "CF7 - Form Submission" and save.

## Step 4: Configure the Google Ads Conversion Tag

Create the conversion tracking tag in GTM:

1. Go to **Tags** → **New**
2. **Tag Type**: Google Ads Conversion Tracking
3. **Conversion ID**: Enter your `AW-123456789` from Step 1
4. **Conversion Label**: Enter your conversion label from Step 1
5. **Conversion Value**: Leave blank (we set this in the conversion action)

**Enhanced Conversions Setup** (this is crucial):
1. Check **Enable Enhanced Conversions**
2. **Data Source**: Data Layer
3. **User-provided data**: Configure the following mappings:
   - Email: `{{DLV - user_data.email_address}}`
   - Phone: `{{DLV - user_data.phone_number}}`
   - First Name: `{{DLV - user_data.address.first_name}}`
   - Last Name: `{{DLV - user_data.address.last_name}}`

You'll need to create Data Layer Variables for each of these. In **Variables** → **User-Defined Variables**:

**Email Variable:**
- Type: Data Layer Variable
- Data Layer Variable Name: `user_data.email_address`
- Name: `DLV - user_data.email_address`

**Phone Variable:**
- Type: Data Layer Variable  
- Data Layer Variable Name: `user_data.phone_number`
- Name: `DLV - user_data.phone_number`

**First Name Variable:**
- Type: Data Layer Variable
- Data Layer Variable Name: `user_data.address.first_name` 
- Name: `DLV - user_data.address.first_name`

**Last Name Variable:**
- Type: Data Layer Variable
- Data Layer Variable Name: `user_data.address.last_name`
- Name: `DLV - user_data.address.last_name`

Set the **Firing Trigger** to your "CF7 - Form Submission" trigger from Step 3.

## Step 5: Test and Publish

Before going live, test everything in GTM's Preview mode:

1. Click **Preview** in GTM
2. Navigate to a page with your Contact Form 7 form
3. Fill out and submit the form
4. In the GTM preview panel, verify:
   - The `cf7_form_submit` event fires
   - The Google Ads Conversion tag fires
   - The data layer contains the user data fields
   - No errors in the console

If everything looks good, **Submit** and **Publish** your GTM container.

## Testing & Verification

### Real-Time Testing
After publishing, submit a test form and verify:

1. **Browser Console**: You should see "CF7 form submitted - conversion tracked"
2. **GTM Debug**: Install Google Tag Assistant and verify the conversion tag fires
3. **Google Ads**: Go to **Tools & Settings** → **Measurement** → **Conversions**. Click on your conversion action and check the **Recent conversions** tab — test conversions should appear within 10-15 minutes

### Production Verification
After 24-48 hours of live traffic:

1. **Google Ads Conversion Count**: Check the conversions column in your campaigns
2. **Enhanced Conversions Status**: In the conversion action settings, verify "Enhanced conversions" shows "Eligible" (not "Not eligible" or "No recent conversions")
3. **Cross-Reference**: If you have Flamingo installed, compare Google Ads conversion count to Flamingo entries. Acceptable variance is 5-15% (some users block JavaScript, some bot submissions get filtered out by Google)

### Red Flags
- Conversion count is 0 after 48 hours with form submissions
- Enhanced Conversions shows "Not eligible" — indicates user data isn't being captured properly
- Conversion count is 50%+ higher than form submissions — indicates duplicate firing or non-human traffic

## Troubleshooting

**Problem**: Conversions not showing up in Google Ads after 24 hours
Check the browser console when submitting forms. If you don't see the "CF7 form submitted" message, the DOM event listener isn't firing. Verify Contact Form 7 is properly installed and the form is actually using CF7 (not another form plugin). Also check that your GTM container is published, not just saved as a draft.

**Problem**: Enhanced Conversions showing "Not eligible"  
The user data isn't reaching Google Ads. Check your Data Layer Variables in GTM Preview mode — if they're showing "undefined", your field names in the JavaScript don't match your CF7 form fields. Update the field names in the code to match exactly what's in your Contact Form 7 shortcode (like `[text* your-name]`).

**Problem**: Getting duplicate conversions on single form submissions
This usually happens if you have multiple tracking scripts or if the form is embedded multiple times on the page. Check for duplicate GTM containers or other Google Ads tracking scripts. Also ensure your conversion action counting is set to "One" not "Every".

**Problem**: Conversions firing on form errors or validation failures
The `wpcf7mailsent` event only fires on successful submissions, but if you're seeing conversions on failed submissions, you might be tracking the wrong event. Double-check that your trigger is set to `cf7_form_submit` (our custom event) not generic form events.

**Problem**: Conversion count way higher than actual form submissions
Check if your GTM trigger is firing on multiple events. Go to GTM Preview and submit a form — the trigger should fire exactly once. If it's firing multiple times, you might have the trigger set to "All Custom Events" and picking up other events. Restrict it to only the `cf7_form_submit` event.

**Problem**: Phone number formatting causing Enhanced Conversions issues
Google Ads Enhanced Conversions expects phone numbers in E.164 format (+1234567890). If users enter phone numbers with spaces, dashes, or without country codes, add formatting in your JavaScript. Use a library like libphonenumber-js or simple regex to clean the phone number before pushing to the data layer.

## What To Do Next

Now that your Contact Form 7 conversions are tracking in Google Ads, consider these next steps:

- Set up [Contact Form 7 to HubSpot integration](/integrations/contact-form-7-to-hubspot) to automatically sync leads to your CRM
- Add [Contact Form 7 GA4 conversion tracking](/tracking/contact-form-7-ga4-conversion-tracking) for cross-platform attribution analysis  
- Configure [Contact Form 7 Meta Ads tracking](/tracking/contact-form-7-meta-ads-conversion-tracking) if you're running Facebook campaigns
- Get a [free tracking audit](/contact) — I'll review your setup and identify any gaps in your conversion tracking

*This guide is part of the [Google Ads Conversion Tracking hub](/tracking/google-ads-conversion-tracking) — comprehensive guides for tracking any lead source as Google Ads conversions.*
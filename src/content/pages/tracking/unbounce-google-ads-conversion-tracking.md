---
title: "How to Track Unbounce Conversions in Google Ads (2026 Guide)"
slug: "unbounce-google-ads-conversion-tracking"
description: "Step-by-step guide to tracking Unbounce form submissions as conversions in Google Ads. Covers GTM setup, Enhanced Conversions, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/google-ads-conversion-tracking"
page_type: "spoke"
---

# Unbounce + Google Ads Conversion Tracking Setup

I see this setup broken in about 35% of accounts I audit. The issue? Most people either rely on Unbounce's native Google Ads integration (which doesn't support Enhanced Conversions) or try to track conversions through redirect URLs, missing 20-30% of actual form submissions. Here's how to set it up properly using GTM and Enhanced Conversions.

## What You'll Have Working By The End

- Form submissions from Unbounce pages firing as conversions in Google Ads with first-party user data
- Enhanced Conversions enabled for improved attribution and iOS 14.5+ recovery
- Cross-platform attribution working correctly when users convert on different devices
- Accurate conversion counts matching your Unbounce lead exports (within 5-15% variance)
- Proper conversion values and lead scoring if you're running Smart Bidding

## Prerequisites

- [ ] Google Ads account with Editor access or above
- [ ] Google Tag Manager container with Publish permissions
- [ ] Unbounce account with ability to edit page scripts
- [ ] Access to your Unbounce form submission data for verification
- [ ] Customer email/phone data being collected in your Unbounce forms

## Step 1: Create the Google Ads Conversion Action

Log into Google Ads and navigate to Goals > Conversions. Click the plus button and select "Website."

Set these specific values:
- **Category**: Lead (not Purchase)
- **Conversion name**: "Unbounce Form Submit" or your specific form name
- **Value**: Use the same value for each conversion (I typically set $50-100 for B2B leads)
- **Count**: One (crucial for lead gen - you don't want duplicate counting)
- **Attribution window**: 30 days click, 1 day view (default is fine)
- **Include in Conversions**: Yes

After saving, you'll get a Conversion ID (format: AW-123456789) and Conversion Label (format: AbCdEfGhIj). Copy both - you'll need them for GTM.

## Step 2: Set Up Unbounce Form Event Tracking

Unbounce fires a `ub-form-success` event when forms are submitted successfully, but you need to capture the form data for Enhanced Conversions.

Add this script to your Unbounce page's "Javascript" section:

```javascript
// Enhanced conversion data collection for Unbounce
window.addEventListener('message', function(event) {
  if (event.data.type === 'ub-form-success') {
    // Get form data from the submission
    const formData = event.data.formData;
    
    // Push enhanced conversion data to dataLayer
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      'event': 'unbounce_form_submit',
      'form_name': event.data.variant || 'default',
      'page_name': lp.jQuery('title').text(),
      'user_data': {
        'email_address': formData.email || '',
        'phone_number': formData.phone || formData.phone_number || '',
        'first_name': formData.first_name || formData.fname || '',
        'last_name': formData.last_name || formData.lname || '',
        'address': {
          'city': formData.city || '',
          'region': formData.state || formData.region || '',
          'postal_code': formData.zip || formData.postal_code || '',
          'country': formData.country || ''
        }
      }
    });
  }
});

// Backup method for older Unbounce implementations
lp.jQuery(function($) {
  $('.lp-pom-form').on('submit', function() {
    setTimeout(function() {
      if (window.location.hash === '#lp-pom-form-success' || $('.lp-pom-form-success').is(':visible')) {
        // Extract form data if the event listener didn't fire
        const formElement = $('.lp-pom-form')[0];
        const formData = new FormData(formElement);
        
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
          'event': 'unbounce_form_submit_backup',
          'user_data': {
            'email_address': formData.get('email') || '',
            'phone_number': formData.get('phone') || '',
            'first_name': formData.get('first_name') || '',
            'last_name': formData.get('last_name') || ''
          }
        });
      }
    }, 1000);
  });
});
```

Make sure your GTM container is loaded on the Unbounce page by adding the GTM snippet to the "Head Scripts" section.

## Step 3: Configure GTM Trigger and Variables

In GTM, create a Custom Event trigger:
- **Trigger Type**: Custom Event
- **Event name**: `unbounce_form_submit`
- **This trigger fires on**: All Custom Events

Create these Built-In Variables (if not already enabled):
- Page URL
- Page Title

Create these User-Defined Variables for Enhanced Conversions:
1. **Email Variable**:
   - **Variable Type**: Data Layer Variable
   - **Data Layer Variable Name**: `user_data.email_address`

2. **Phone Variable**:
   - **Variable Type**: Data Layer Variable
   - **Data Layer Variable Name**: `user_data.phone_number`

3. **First Name Variable**:
   - **Variable Type**: Data Layer Variable
   - **Data Layer Variable Name**: `user_data.first_name`

## Step 4: Create Google Ads Conversion Tag

Create a new tag in GTM:
- **Tag Type**: Google Ads Conversion Tracking
- **Conversion ID**: Your AW-123456789 number (without "AW-")
- **Conversion Label**: Your conversion label from Step 1
- **Conversion Value**: Use a constant value or variable if dynamic
- **Transaction ID**: Leave blank (not needed for leads)

For Enhanced Conversions, expand "Enhanced Conversions" and set:
- **User-provided data**: Variables from Data Layer
- **Email**: {{Email Variable}}
- **Phone**: {{Phone Variable}}
- **First Name**: {{First Name Variable}}
- **Last Name**: {{user_data.last_name}} (enter directly)

Set the trigger to fire on your `unbounce_form_submit` event.

## Step 5: Enable Enhanced Conversions in Google Ads

Back in Google Ads, go to Goals > Conversions and click on your conversion action.

Click "Edit settings" and scroll to "Enhanced conversions":
- Turn on Enhanced conversions for leads
- Select "Google Tag Manager" as your setup method
- Accept the customer data terms

This tells Google Ads to expect Enhanced Conversion data from your GTM tags.

## Testing & Verification

**Preview Mode Testing:**
1. Enable Preview mode in GTM and visit your Unbounce page
2. Fill out and submit the form
3. Check that the `unbounce_form_submit` event fires in the GTM debugger
4. Verify the Google Ads conversion tag fires with user data populated

**Google Ads Verification:**
1. Go to Google Ads > Goals > Conversions
2. Look for "Recent conversions" - test submissions should appear within 3 hours
3. Check the "Enhanced conversions" column shows "Receiving enhanced conversions"
4. Click into the conversion action to see individual conversion details

**Cross-Reference Numbers:**
Compare your Unbounce lead exports with Google Ads conversion counts over a 7-day period. Acceptable variance is 5-15%. Higher variance usually indicates:
- Ad blockers preventing GTM from loading (15-25% of traffic)
- Form submissions not triggering the success event properly
- Users submitting multiple times (check your "Count" setting)

## Troubleshooting

**Problem**: GTM debugger shows the event firing but no conversion appears in Google Ads
GTM preview mode doesn't always reflect actual user behavior. Check that your Conversion ID doesn't include the "AW-" prefix in the GTM tag - it should just be the numbers. Also verify Enhanced Conversions is enabled in Google Ads, not just GTM.

**Problem**: Enhanced Conversions shows "Not receiving enhanced conversions" despite user data being collected
This usually means the email format is wrong or empty. Check your Data Layer Variable is pulling `user_data.email_address` exactly. Email must be properly formatted (no spaces, valid @ symbol). Phone numbers need country codes for international traffic.

**Problem**: Conversion count is 2-3x higher than actual form submissions
Your conversion action is set to "Every" instead of "One" per click. Go to Google Ads conversion settings and change the count setting. For lead gen, you want "One" conversion per ad click, not per submission event.

**Problem**: Unbounce form success event isn't firing consistently
Some Unbounce templates don't trigger the `ub-form-success` message properly. Use the backup jQuery method in the code above, or switch to tracking via the success URL redirect method. Check if your form has custom success actions that bypass the default event.

**Problem**: iOS traffic showing much lower conversion rates than Android
This is normal post-iOS 14.5, but Enhanced Conversions helps. Make sure you're collecting email addresses on the form - Google can match these for attribution even when tracking is blocked. Consider implementing Conversions API for Facebook if you're running cross-platform campaigns.

**Problem**: Test conversions not appearing in Google Ads after 6+ hours
Check if your Google Ads account has conversion delays due to high invalid traffic filtering. B2B accounts with expensive keywords often get delayed reporting. Also verify your GTM container is published (not just previewed) and the live page is firing events correctly.

## What To Do Next

Once your Unbounce + Google Ads tracking is working, consider these related setups:

- [Unbounce + Meta Ads conversion tracking](/tracking/unbounce-meta-ads-conversion-tracking) for cross-platform attribution
- [Unbounce + GA4 conversion tracking](/tracking/unbounce-ga4-conversion-tracking) to get a complete view of your funnel
- [Unbounce to HubSpot integration](/integrations/unbounce-to-hubspot) to sync your leads automatically

Need help auditing your current setup? I offer [free tracking audits](/contact) for qualified businesses spending $10k+ per month on Google Ads.

*This guide is part of the [Google Ads Conversion Tracking hub](/tracking/google-ads-conversion-tracking) — comprehensive tracking setups for every major form and landing page platform.*
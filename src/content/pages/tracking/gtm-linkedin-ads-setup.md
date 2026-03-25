---
title: "Client-Side GTM for LinkedIn Ads: Complete Setup Guide (2026)"
slug: "gtm-linkedin-ads-setup"
description: "Complete guide to setting up Client-Side GTM for LinkedIn Ads. Step-by-step configuration, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/form-conversion-tracking"
page_type: "spoke"
---

# Client-Side GTM + LinkedIn Ads Setup Guide

LinkedIn's Insight Tag through client-side GTM is deceptively simple to set up but brutally easy to break. I see this configuration in about 60% of B2B accounts I audit, and roughly half of them are either firing duplicate events or missing conversions entirely because someone copied the wrong event ID or set up form tracking that only works on one page.

The biggest issue? LinkedIn's conversion tracking requires specific event names and partner IDs that most people get wrong on the first try, then wonder why their attribution is showing 30% fewer conversions than their CRM.

## What You'll Have Working By The End

- LinkedIn Insight Tag properly installed and firing on all pages
- Conversion events (leads, purchases, sign-ups) tracking with accurate values
- Cross-domain tracking if you have multiple domains or subdomains
- Form submissions automatically captured and sent to LinkedIn as conversions
- Attribution data flowing correctly into LinkedIn Campaign Manager

## Prerequisites

- [ ] LinkedIn Campaign Manager access with conversion tracking permissions
- [ ] Google Tag Manager container already installed on your site
- [ ] LinkedIn Partner ID from your Campaign Manager account (found in Account Assets > Insight Tag)
- [ ] List of conversion events you want to track (form fills, purchases, downloads, etc.)
- [ ] Access to modify your website's dataLayer (if using custom events)

## Step 1: Install the LinkedIn Insight Tag

First, grab your Partner ID from LinkedIn Campaign Manager. Go to Account Assets > Insight Tag and copy the numeric ID (not the full script).

In GTM, create a new Custom HTML tag:

```javascript
<script type="text/javascript">
_linkedin_partner_id = "YOUR_PARTNER_ID";
window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
window._linkedin_data_partner_ids.push(_linkedin_partner_id);
</script>
<script type="text/javascript">
(function(l) {
if (!l){window.lintrk = function(a,b){window.lintrk.q.push([a,b])};
window.lintrk.q=[]}
var s = document.getElementsByTagName("script")[0];
var b = document.createElement("script");
b.type = "text/javascript";b.async = true;
b.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js";
s.parentNode.insertBefore(b, s);})(window.lintrk);
</script>
<noscript>
<img height="1" width="1" style="display:none;" alt="" src="https://px.ads.linkedin.com/collect/?pid=YOUR_PARTNER_ID&fmt=gif" />
</noscript>
```

Replace `YOUR_PARTNER_ID` with your actual Partner ID (just the numbers, no quotes).

Set the trigger to "All Pages" and name the tag "LinkedIn Insight Tag - Base Code".

**Important:** Don't use LinkedIn's auto-generated GTM tag from their interface. It's outdated and missing the partner ID array setup that's required for proper attribution.

## Step 2: Set Up Conversion Events

LinkedIn needs specific event names to match your conversion goals in Campaign Manager. The most common events are:

- `lead` - Form submissions, newsletter signups
- `purchase` - Actual purchases with revenue
- `sign_up` - Account registrations
- `contact` - Contact form submissions
- `download` - Resource downloads

Create a new Custom HTML tag for each conversion type:

```javascript
<script type="text/javascript">
window.lintrk('track', { 
  conversion_id: 'CONVERSION_ID_HERE',
  conversion_url_match: 'exact'  // or 'contains'
});
</script>
```

For e-commerce with revenue tracking:

```javascript
<script type="text/javascript">
window.lintrk('track', { 
  conversion_id: 'CONVERSION_ID_HERE',
  conversion_value: {{Transaction Value}},
  currency: 'USD'
});
</script>
```

The `conversion_id` comes from LinkedIn Campaign Manager > Conversions. Each conversion action gets its own ID.

**Which approach should you use?** URL-based tracking works for simple thank-you pages. For complex forms or single-page apps, use dataLayer events with custom triggers.

## Step 3: Configure Form Tracking (Most Common Setup)

For form submissions, I typically use GTM's built-in Form Submission trigger instead of relying on redirect URLs. This catches forms that submit via AJAX or don't redirect.

Create a Form Submission trigger:
- Trigger Type: Form Submission
- Wait for Tags: Enabled (2000ms timeout)
- Check Validation: Enabled
- Fire On: Some Forms
- Form URL contains your domain (prevents tracking external forms)

Then modify your conversion tag to use form-specific data:

```javascript
<script type="text/javascript">
window.lintrk('track', { 
  conversion_id: 'YOUR_CONVERSION_ID',
  email: {{Form Email}},  // if available in dataLayer
  conversion_url: {{Page URL}}
});
</script>
```

**Common mistake:** Don't fire conversion tags on the form page itself. Fire them after submission is confirmed, either on a thank-you page or via a successful form submission event.

## Step 4: Set Up Cross-Domain Tracking (If Needed)

If your funnel spans multiple domains (like example.com → checkout.example.com or separate landing page domains), you need to configure cross-domain tracking.

Add this to your base LinkedIn tag (before the closing script tag):

```javascript
lintrk('set', 'allowLinkedInLead', true);
```

Then make sure your GTM container is installed on all domains in the funnel. LinkedIn's pixel will automatically handle cross-domain attribution as long as the same Partner ID is used everywhere.

**Which domains need tracking?** Any domain where users can land from LinkedIn ads OR where conversions happen. If someone lands on domain A but converts on domain B, both need the pixel.

## Step 5: Add Enhanced Matching (Recommended)

If you capture email addresses, phone numbers, or other user data, pass it to LinkedIn for better attribution:

```javascript
<script type="text/javascript">
window.lintrk('track', { 
  conversion_id: 'YOUR_CONVERSION_ID',
  user_data: {
    email: {{User Email}},
    phone: {{User Phone}},
    first_name: {{User First Name}},
    last_name: {{User Last Name}},
    company_name: {{User Company}}
  }
});
</script>
```

The email should be hashed SHA256 client-side if you're concerned about PII:

```javascript
// Add this function to hash emails
function hashEmail(email) {
  return CryptoJS.SHA256(email.toLowerCase().trim()).toString();
}

// Then use it in the conversion tag
email: hashEmail({{User Email}})
```

## Testing & Verification

**GTM Preview Mode:**
1. Enable Preview mode in GTM
2. Visit your site and trigger a conversion
3. Check that both the base LinkedIn tag and conversion tag fire
4. Look for the network request to `snap.licdn.com` in DevTools

**LinkedIn Campaign Manager:**
1. Go to Account Assets > Insight Tag
2. Check "Active on Domain" status (should show green within 15 minutes)
3. Go to Conversions and check "Recent Activity" 
4. Test conversions should appear within 1-2 hours

**Browser DevTools:**
- Look for `li_fat_id` cookie being set
- Check for JavaScript errors in console
- Network tab should show successful calls to LinkedIn's endpoints

**Acceptable variance:** LinkedIn typically shows 5-10% fewer conversions than your analytics due to ad blockers and attribution windows. If you're seeing 20%+ discrepancy, something is misconfigured.

**Red flags:**
- No `li_fat_id` cookie means the base tag isn't firing
- Conversion events firing on every page load instead of actual conversions
- Multiple conversion events for the same user action (duplicate tracking)

## Troubleshooting

**Problem:** Base tag installed but showing "Not recently active" in Campaign Manager
Check that you're using the numeric Partner ID, not the full script. Also verify GTM container is published and actually loading on your pages. I see this when people test in Preview mode but forget to submit and publish the container.

**Problem:** Conversions firing on page load instead of form submission
Your trigger is probably set to "All Pages" instead of "Form Submission" or your custom event. Double-check the trigger configuration and make sure you're using the right trigger type for your conversion event.

**Problem:** Duplicate conversions showing in LinkedIn
Usually caused by multiple tags firing for the same event, or firing both on form submission AND thank-you page. Set up proper trigger conditions to prevent double-firing, or use GTM's built-in deduplication.

**Problem:** Cross-domain tracking not working
Make sure GTM container is installed on ALL domains in your funnel, not just the main one. Also verify that LinkedIn's cross-domain settings are enabled in the base tag configuration.

**Problem:** Enhanced matching data not showing in LinkedIn
LinkedIn doesn't show you what enhanced matching data they received - it's used internally for attribution. Test by checking the network request payload in DevTools to confirm the data is being sent properly.

**Problem:** Revenue/value not tracking for e-commerce
Check that your `conversion_value` variable is actually populated and numeric. LinkedIn requires the value to be a number, not a string with currency symbols. Use GTM's built-in e-commerce variables or create custom variables that format the data correctly.

## What To Do Next

Now that your LinkedIn tracking is working, consider implementing [server-side form tracking](/tracking/server-side-form-tracking) for better data quality and ad blocker resistance. You might also want to set up [HubSpot form integration](/tracking/hubspot-form-tracking) if you're using HubSpot for lead management.

For a comprehensive audit of your tracking setup across all platforms, [contact me for a free tracking audit](/contact) — I'll review your LinkedIn implementation along with your other ad platforms and identify any gaps.

*This guide is part of the [Form Conversion Tracking Hub](/tracking/form-conversion-tracking) — complete guides for tracking form conversions across all major ad platforms.*
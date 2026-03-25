---
title: "How to Track Calendly Conversions in GA4 (2026 Guide)"
slug: "calendly-ga4-conversion-tracking"
description: "Step-by-step guide to tracking Calendly form submissions as conversions in GA4. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/ga4-conversion-tracking"
page_type: "spoke"
---

# Calendly + GA4 Conversion Tracking Setup

Most Calendly + GA4 setups I audit are missing about 30-40% of conversions because they're only tracking the thank you page load, not the actual booking event. Calendly fires a JavaScript event when someone completes a booking — but if you don't catch it properly, you'll never know how many leads your ads are actually generating.

The setup I'm about to show you captures the actual `calendly.event_scheduled` event that fires when someone books a meeting, whether Calendly is embedded on your site or used as a popup.

## What You'll Have Working By The End

- Calendly bookings tracked as `generate_lead` conversions in GA4
- Conversion events firing immediately when someone books (not just on thank you page)
- Clean conversion data that matches your actual Calendly booking count
- Proper attribution to your marketing campaigns and traffic sources
- GA4 conversions ready to import into Google Ads if needed

## Prerequisites

- [ ] Calendly account with your booking page configured
- [ ] GA4 property set up and receiving basic traffic data
- [ ] Google Tag Manager container installed on your website
- [ ] Editor access to GTM and Admin access to GA4
- [ ] Calendly embedded on your site or used via popup (not just direct links to calendly.com)

## Step 1: Set Up the Calendly Event Listener

First, you need to capture Calendly's native JavaScript event. Add this custom HTML tag to GTM that listens for the `calendly.event_scheduled` event:

Create a new Custom HTML tag in GTM with this code:

```html
<script>
window.addEventListener('message', function(e) {
  if (e.data.event && e.data.event.indexOf('calendly') === 0) {
    console.log('Calendly event detected:', e.data.event);
    
    if (e.data.event === 'calendly.event_scheduled') {
      // Push to data layer for GTM
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        'event': 'calendly_booking_completed',
        'calendly_event_type': e.data.event,
        'calendly_invitee': e.data.payload ? e.data.payload.invitee : null,
        'calendly_event_uri': e.data.payload ? e.data.payload.event.uri : null
      });
      
      console.log('Calendly booking event pushed to dataLayer');
    }
  }
});
</script>
```

Set the trigger to "All Pages" since someone could book from any page where Calendly is embedded.

## Step 2: Create the Data Layer Trigger

Create a new Custom Event trigger in GTM:
- **Trigger Type**: Custom Event
- **Event Name**: `calendly_booking_completed`
- **This trigger fires on**: All Custom Events

Name it "Calendly - Booking Completed" so you can find it easily later.

## Step 3: Configure the GA4 Event Tag

Create a new GA4 Event tag in GTM:
- **Tag Type**: Google Analytics: GA4 Event
- **Configuration Tag**: Select your GA4 Configuration tag
- **Event Name**: `generate_lead`

Add these Event Parameters:
- **method**: `calendly`
- **content_group1**: `{{Page URL}}`
- **custom_data**: `calendly_booking`

The `generate_lead` event is Google's recommended event for lead generation forms. Using it instead of a custom event means GA4 will automatically classify it properly in your reports.

Set the trigger to your "Calendly - Booking Completed" trigger from Step 2.

## Step 4: Mark as Conversion in GA4

In GA4, go to Configure → Events. You should see your `generate_lead` events appearing (you might need to wait 24 hours or trigger a test booking first).

Click the toggle next to `generate_lead` to mark it as a conversion. If you're running Google Ads, this conversion will be available for import into your Google Ads account.

## Step 5: Set Up Enhanced Measurement (Optional but Recommended)

While you're in GA4, verify Enhanced Measurement is enabled (Configure → Data Streams → your website → Enhanced measurement). This ensures you're getting proper page view and engagement data to attribute the conversion correctly.

I recommend leaving all Enhanced Measurement toggles on — the additional context helps with proper attribution when someone books after browsing multiple pages.

## Testing & Verification

### In GTM Preview Mode
1. Open GTM Preview mode and load a page with your Calendly embed
2. Complete a test booking (use your own email)
3. Check the GTM Preview panel — you should see:
   - Custom HTML tag fired on page load
   - Custom Event trigger fired after booking
   - GA4 Event tag fired with your `generate_lead` event

### In GA4 DebugView
1. Go to GA4 → Configure → DebugView
2. Complete another test booking
3. You should see the `generate_lead` event appear in real-time
4. Click into the event to verify the parameters are populated correctly

### In GA4 Realtime Reports
Check GA4 → Reports → Realtime. Your `generate_lead` events should appear under "Event count by Event name" within 1-2 minutes.

### Cross-Check Numbers
After running for a week, compare:
- GA4 `generate_lead` conversion count
- Calendly dashboard booking count
- Your CRM lead count (if you're using webhooks to sync)

Acceptable variance is 5-15%. If you're seeing more than 20% difference, something's broken.

## Troubleshooting

**Problem**: GTM Preview shows the Custom HTML tag firing but no data layer event
→ Check your browser console for JavaScript errors. Calendly might not be fully loaded when the listener is set up. Try wrapping the code in a `setTimeout` function with a 2-second delay.

**Problem**: Events showing in DebugView but not in standard GA4 reports after 24 hours
→ Your GA4 property might have filters or internal traffic exclusion rules. Check Configure → Data Settings → Data Filters. Also verify you're looking at the correct date range.

**Problem**: Getting duplicate events (2-3 conversions per booking)
→ Your Custom HTML tag is probably firing on multiple page types. Change the trigger from "All Pages" to only pages where Calendly is actually embedded. Or add a check to prevent multiple executions.

**Problem**: Events not firing for popup Calendly bookings
→ The popup version uses a slightly different event structure. Modify your event listener to also catch `calendly.event_type_viewed` events and filter for the right event type.

**Problem**: Conversions showing up but not attributing to the right traffic source
→ GA4 uses a 90-day attribution window by default. If someone visited from an ad 30 days ago and booked today, it might still attribute to that ad. Check your attribution settings in GA4 → Configure → Attribution Settings.

**Problem**: Test bookings working but real bookings not tracking
→ Some ad blockers specifically block Calendly's postMessage events. This affects about 15-25% of users. Consider setting up server-side tracking using Calendly's webhooks as a backup.

## What To Do Next

This setup gets you solid GA4 conversion tracking, but you'll probably want to expand it:

- [Set up Calendly tracking for Google Ads](/tracking/calendly-google-ads-conversion-tracking) if you're running search or display campaigns
- [Connect Calendly to HubSpot](/integrations/calendly-to-hubspot) for complete lead lifecycle tracking
- [Track Calendly conversions in Meta Ads](/tracking/calendly-meta-ads-conversion-tracking) if you're running Facebook/Instagram campaigns

Having issues with your current tracking setup? I audit tracking implementations like this one all the time — [get a free tracking audit](/contact) and I'll tell you exactly what's broken and how to fix it.

*This guide is part of the [GA4 Conversion Tracking Hub](/tracking/ga4-conversion-tracking) — complete guides for tracking form submissions, purchases, and lead generation in Google Analytics 4.*
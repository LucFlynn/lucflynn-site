---
title: "How to Track Calendly Conversions in Google Ads (2026 Guide)"
slug: "calendly-google-ads-conversion-tracking"
description: "Step-by-step guide to tracking Calendly form submissions as conversions in Google Ads. Covers GTM setup, Enhanced Conversions, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/google-ads-conversion-tracking"
page_type: "spoke"
---

# Calendly + Google Ads Conversion Tracking Setup

Calendly bookings not showing up as Google Ads conversions is one of the most common tracking gaps I see. The problem? Calendly's event firing happens in an iframe or popup that your standard conversion tracking can't see. I've fixed this setup in about 60 accounts where leads were booking meetings but Google Ads had no idea those high-value conversions were happening.

The good news is Calendly fires a reliable `calendly.event_scheduled` postMessage event that we can catch with GTM. Combined with Enhanced Conversions for better attribution, this gives you proper lead tracking that actually matches your CRM.

## What You'll Have Working By The End

- Calendly bookings firing as Google Ads conversions within seconds of scheduling
- Enhanced Conversions passing email data for better attribution through iOS 14.5+ blocks  
- Proper conversion counting (One per booking, not multiple if they refresh)
- Cross-platform attribution working when users book on mobile after clicking ads on desktop
- Accurate ROI data in Google Ads that matches your actual meeting bookings

## Prerequisites

- [ ] Google Ads account with conversion tracking enabled
- [ ] GTM container installed on pages where Calendly appears
- [ ] Calendly embed or popup on your site (doesn't work with redirect-only flows)
- [ ] Admin access to Google Ads to create conversion actions
- [ ] Email addresses available in your booking flow (required for Enhanced Conversions)

## Step 1: Create the Google Ads Conversion Action

First, set up the conversion action that will receive your Calendly data.

In Google Ads, go to Goals → Conversions → "+" New Conversion Action → Website:

- **Conversion Name**: "Calendly Booking" or "Meeting Scheduled"  
- **Value**: Don't assign a value (unless you have specific lead values)
- **Count**: One (crucial — you want one conversion per meeting, not per page view)
- **Attribution Window**: 30 days click, 1 day view (default is fine)
- **Category**: Lead or Sign-up

Save this and note your **Conversion ID** and **Conversion Label** — you'll need both for GTM.

## Step 2: Set Up the Calendly Event Listener in GTM

Create a Custom HTML tag in GTM to listen for Calendly's postMessage event:

```javascript
<script>
window.addEventListener('message', function(e) {
  if (e.data.event && e.data.event.indexOf('calendly') === 0) {
    if (e.data.event === 'calendly.event_scheduled') {
      
      // Extract invitee data if available
      var inviteeData = e.data.event_details.invitee || {};
      var inviteeEmail = inviteeData.email || '';
      var inviteeName = inviteeData.name || '';
      
      // Fire conversion event to dataLayer
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        'event': 'calendly_booking_complete',
        'calendly_invitee_email': inviteeEmail,
        'calendly_invitee_name': inviteeName,
        'calendly_event_type': e.data.event_details.event_type.name || '',
        'calendly_meeting_start': e.data.event_details.event.start_time || ''
      });
      
      console.log('Calendly booking tracked:', e.data.event_details);
    }
  }
});
</script>
```

**Tag Configuration**:
- Tag Type: Custom HTML
- Trigger: All Pages (where Calendly appears)
- **Important**: Check "Support document.write" in Advanced Settings

This catches the postMessage event and pushes clean data to the dataLayer that GTM can work with.

## Step 3: Create the GTM Trigger

Create a Custom Event trigger for when Calendly bookings happen:

- **Trigger Type**: Custom Event
- **Event Name**: `calendly_booking_complete`
- **This trigger fires on**: All Custom Events

Save as "Calendly Booking Complete".

## Step 4: Set Up Enhanced Conversions Variables

Create these dataLayer variables to pass email data to Google Ads:

**Variable 1: Calendly Email**
- Variable Type: Data Layer Variable  
- Data Layer Variable Name: `calendly_invitee_email`
- Name: "Calendly - Invitee Email"

**Variable 2: Calendly Name**  
- Variable Type: Data Layer Variable
- Data Layer Variable Name: `calendly_invitee_name`  
- Name: "Calendly - Invitee Name"

## Step 5: Create the Google Ads Conversion Tag

Now create the conversion tag that sends data to Google Ads:

- **Tag Type**: Google Ads Conversion Tracking
- **Conversion ID**: [Your conversion ID from Step 1]
- **Conversion Label**: [Your conversion label from Step 1] 
- **Conversion Value**: Leave blank (or set dynamic value if you have lead scoring)

**Enhanced Conversions Settings**:
- Enable Enhanced Conversions: ✓
- User-Provided Data → Email: `{{Calendly - Invitee Email}}`
- User-Provided Data → First Name: Extract first name from `{{Calendly - Invitee Name}}`

**Trigger**: Calendly Booking Complete (from Step 3)

The Enhanced Conversions setup is crucial here — about 25% of your Calendly users will be on iOS or have strict cookie blocking. Enhanced Conversions lets Google match conversions to ad clicks using email hashing even when third-party cookies fail.

## Step 6: Handle First Name Extraction (Optional but Recommended)

For better Enhanced Conversions matching, extract the first name:

Create a Custom JavaScript variable:

```javascript
function() {
  var fullName = {{Calendly - Invitee Name}} || '';
  var firstName = fullName.split(' ')[0] || '';
  return firstName.trim();
}
```

Use this variable in your Enhanced Conversions "First Name" field instead of the full name.

## Testing & Verification

### GTM Preview Mode Testing
1. Enable GTM Preview mode and go to a page with Calendly
2. Book a test meeting using a real email address
3. In GTM Preview, look for:
   - "calendly_booking_complete" event firing
   - Your Google Ads conversion tag firing
   - dataLayer variables populated with email/name data

### Google Ads Verification
1. Go to Google Ads → Goals → Conversions
2. Your conversion should show "Recorded today: 1" within 15-30 minutes
3. Click into the conversion to see if Enhanced Conversions data was received
4. Status should show "Enhanced conversions enabled" with green checkmark

### Cross-Check Your Numbers
Compare these data points weekly:
- Calendly dashboard: Total meetings scheduled
- Google Ads conversions: Total conversion count  
- **Acceptable variance**: 5-15% (some users book directly without clicking ads)

Red flags: If Google Ads shows 40%+ fewer conversions than Calendly bookings, your tracking is broken.

## Troubleshooting

**Problem**: GTM Preview shows the event firing but no conversion tag
**Solution**: Check your trigger event name exactly matches `calendly_booking_complete`. Case sensitive and typos will break this completely.

**Problem**: Enhanced Conversions showing "No user-provided data received"
**Solution**: The email variable is empty. Add a console.log in your Custom HTML to verify `e.data.event_details.invitee.email` contains data. Some Calendly embed configs don't pass invitee data — switch to popup mode.

**Problem**: Conversions showing in Google Ads but attribution is wrong
**Solution**: Enhanced Conversions needs 1-2 hours to process. If still wrong after 24 hours, check that users are booking with the same email they use for Google accounts.

**Problem**: Multiple conversions for single bookings
**Solution**: Your conversion counting is set to "Every" instead of "One". Change this in your Google Ads conversion action settings.

**Problem**: Calendly popup bookings not tracked but embedded form bookings work
**Solution**: The postMessage event origin differs between embed and popup. Add origin checking to your event listener: `if (e.origin.indexOf('calendly.com') > -1)`

**Problem**: Test bookings fire but real user bookings don't show up
**Solution**: Check if your Calendly booking flow includes email collection. If email is optional and users skip it, Enhanced Conversions can't match properly.

## What To Do Next

Once your Calendly + Google Ads tracking is running, consider these related setups:

- [Calendly to HubSpot integration](/integrations/calendly-to-hubspot) for better lead nurturing workflows
- [Calendly + Meta Ads conversion tracking](/tracking/calendly-meta-ads-conversion-tracking) if you're running Facebook campaigns  
- [Calendly + GA4 conversion tracking](/tracking/calendly-ga4-conversion-tracking) for better attribution analysis

Need help auditing your current tracking setup? I offer [free 30-minute tracking audits](/contact) where we'll identify exactly what's broken and prioritize the fixes by revenue impact.

*This guide is part of the [Google Ads Conversion Tracking Hub](/tracking/google-ads-conversion-tracking) — complete conversion tracking setups for 15+ form tools and lead sources.*
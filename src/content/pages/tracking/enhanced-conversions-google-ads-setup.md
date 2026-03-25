---
title: "Enhanced Conversions for Google Ads: Complete Setup Guide (2026)"
slug: "enhanced-conversions-google-ads-setup"
description: "Complete guide to setting up Enhanced Conversions for Google Ads. Step-by-step configuration, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/enhanced-conversions"
page_type: "spoke"
---

# Enhanced Conversions + Google Ads Setup Guide

I audit about 15-20 Google Ads accounts per month, and roughly 60% have Enhanced Conversions either completely broken or capturing maybe 30% of the conversions they should be. The usual culprit? They set up the client-side tag, called it done, and never realized that 20-25% of their users are blocking it entirely.

Enhanced Conversions works by sending hashed customer data (email, phone, address) to Google alongside your conversion events. Google matches this against logged-in users to recover conversions that normal tracking missed. But the implementation is surprisingly nuanced — get the data format wrong and Google just silently ignores it.

## What You'll Have Working By The End

- Enhanced Conversions capturing 85%+ of your actual conversions (vs. 65-70% with standard tracking)
- Both client-side and server-side Enhanced Conversions firing simultaneously for maximum coverage
- Proper PII hashing that actually matches Google's requirements
- Debug setup that lets you see exactly which conversions have enhanced data attached
- Automated data quality validation catching formatting errors before they reach Google

## Prerequisites

- [ ] Google Ads account with conversion tracking already configured
- [ ] Google Tag Manager (GTM) container with existing conversion tags
- [ ] Admin access to Google Ads (need to accept Enhanced Conversions terms)
- [ ] Server-side tagging container (recommended) or ability to deploy Cloud Functions
- [ ] Form data capture working (email minimum, phone/address preferred)

## How Enhanced Conversions Actually Works

Here's the data flow that most people get wrong:

1. **Client-side**: GTM captures form data → hashes PII → sends to Google Ads
2. **Server-side**: Your server captures the same conversion → hashes PII server-side → sends via Conversions API
3. **Google's end**: Deduplicates the two events using gclid + conversion timestamp, keeps the one with better data quality

The key insight: you want both paths firing. Client-side catches users with JavaScript enabled, server-side catches the rest. Google automatically dedupes them.

## Step 1: Enable Enhanced Conversions in Google Ads

In your Google Ads account, navigate to Tools & Settings > Measurement > Conversions. Click on your conversion action.

Under "Enhanced conversions," click "Turn on enhanced conversions." You'll see two options:

- **Google Tag Manager**: Use this if you're doing client-side only (not recommended)
- **Google Ads API or Google Tag Manager**: Choose this for the hybrid approach we're building

Accept the customer data terms. Google will show you a checklist about data handling — actually read this, because violating these terms can get your account suspended.

## Step 2: Configure Client-Side Enhanced Conversions

In GTM, modify your existing Google Ads Conversion Tracking tag:

```javascript
// In your Google Ads Conversion tag, add these fields:
Enhanced Conversion Data = {{Enhanced Conversion Data Variable}}

// Create this variable in GTM:
Variable Type: Custom JavaScript
Variable Name: Enhanced Conversion Data

function() {
  // Capture form data (adjust selectors for your forms)
  var email = document.querySelector('input[type="email"]')?.value;
  var phone = document.querySelector('input[type="tel"]')?.value;
  var firstName = document.querySelector('input[name="first_name"]')?.value;
  var lastName = document.querySelector('input[name="last_name"]')?.value;
  
  // Clean and format the data
  var enhancedData = {};
  
  if (email && email.includes('@')) {
    enhancedData.email = email.toLowerCase().trim();
  }
  
  if (phone) {
    // Remove all non-digits, then format as E.164
    var cleanPhone = phone.replace(/\D/g, '');
    if (cleanPhone.length === 10) {
      enhancedData.phone_number = '+1' + cleanPhone;
    } else if (cleanPhone.length === 11 && cleanPhone.charAt(0) === '1') {
      enhancedData.phone_number = '+' + cleanPhone;
    }
  }
  
  if (firstName) enhancedData.address.first_name = firstName.toLowerCase().trim();
  if (lastName) enhancedData.address.last_name = lastName.toLowerCase().trim();
  
  return Object.keys(enhancedData).length > 0 ? enhancedData : undefined;
}
```

**Important**: Don't hash the data yourself in GTM. Google's tag handles the SHA-256 hashing automatically. I see this mistake in about 30% of setups — they hash it twice and Google can't match anything.

## Step 3: Set Up Server-Side Enhanced Conversions

Deploy a server-side tagging container or Cloud Function. Here's the Cloud Function approach since it's simpler:

```python
import hashlib
import hmac
from google.ads.googleads.client import GoogleAdsClient
import functions_framework

@functions_framework.http
def enhanced_conversion_webhook(request):
    """
    Receives conversion data from your checkout system
    Sends Enhanced Conversion to Google Ads API
    """
    
    # Your conversion data from checkout
    data = request.get_json()
    
    # Hash PII data
    def hash_normalize(value):
        if not value:
            return None
        return hashlib.sha256(value.lower().strip().encode('utf-8')).hexdigest()
    
    # Build the enhanced conversion
    enhanced_conversion = {
        'gclid': data.get('gclid'),  # From URL parameter
        'conversion_action': f'customers/{CUSTOMER_ID}/conversionActions/{CONVERSION_ACTION_ID}',
        'conversion_date_time': data.get('conversion_time'),  # ISO 8601 format
        'conversion_value': float(data.get('value', 0)),
        'currency_code': 'USD'
    }
    
    # Add hashed customer data
    if data.get('email'):
        enhanced_conversion['user_identifiers'] = [
            {
                'hashed_email': hash_normalize(data['email'])
            }
        ]
    
    if data.get('phone'):
        phone = re.sub(r'\D', '', data['phone'])
        if len(phone) == 10:
            phone = '+1' + phone
        elif len(phone) == 11 and phone[0] == '1':
            phone = '+' + phone
        
        enhanced_conversion['user_identifiers'].append({
            'hashed_phone_number': hash_normalize(phone)
        })
    
    # Send to Google Ads
    client = GoogleAdsClient.load_from_storage()
    conversion_upload_service = client.get_service("ConversionUploadService")
    
    response = conversion_upload_service.upload_conversions(
        customer_id=CUSTOMER_ID,
        conversions=[enhanced_conversion],
        partial_failure=True
    )
    
    return {'status': 'success', 'results': len(response.results)}
```

Deploy this to Cloud Functions with these environment variables:
- `GOOGLE_ADS_CUSTOMER_ID`
- `GOOGLE_ADS_CONVERSION_ACTION_ID`
- Path to your Google Ads API credentials JSON

## Step 4: Configure Your Checkout to Send Data

Modify your checkout success page to send conversion data to your Cloud Function:

```javascript
// On checkout success
fetch('https://your-cloud-function-url.cloudfunctions.net/enhanced-conversion-webhook', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    gclid: getUrlParameter('gclid'),  // Capture this on page load and store
    email: checkoutData.email,
    phone: checkoutData.phone,
    value: checkoutData.orderTotal,
    conversion_time: new Date().toISOString()
  })
});

function getUrlParameter(name) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(name);
}
```

**Critical**: You must capture and store the `gclid` parameter from the original ad click, not generate it at conversion time. Store it in localStorage or pass it through your checkout flow.

## Step 5: Test Data Quality Requirements

Google is picky about data formats. Test your hashed data against these requirements:

```javascript
// Email validation
function validateEmail(email) {
  // Must be lowercase, trimmed, valid format
  const cleaned = email.toLowerCase().trim();
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(cleaned) ? cleaned : null;
}

// Phone validation  
function validatePhone(phone) {
  // Must be E.164 format (+1234567890)
  const cleaned = phone.replace(/\D/g, '');
  if (cleaned.length === 10) {
    return '+1' + cleaned;
  } else if (cleaned.length === 11 && cleaned[0] === '1') {
    return '+' + cleaned;
  }
  return null;
}

// Address validation (optional but helps match rate)
function validateAddress(address) {
  return {
    first_name: address.firstName?.toLowerCase().trim(),
    last_name: address.lastName?.toLowerCase().trim(),
    street: address.street?.toLowerCase().trim(),
    city: address.city?.toLowerCase().trim(),
    region: address.state?.toLowerCase().trim(),
    postal_code: address.zip?.trim(),
    country: address.country?.toLowerCase().trim()
  };
}
```

I recommend validating data quality before sending to Google. Invalid formats just get ignored silently, and you'll never know your match rate is suffering.

## Testing & Verification

### GTM Preview Mode
Enable GTM Preview mode and trigger a test conversion. In the debug panel:

1. Find your Google Ads Conversion tag
2. Look for "Enhanced Conversion Data" in the tag details
3. Verify it shows the structured data (not hashed yet)
4. Check that email format looks correct (lowercase, trimmed)

### Google Ads Interface
In Google Ads, go to Tools & Settings > Measurement > Conversions. Click on your conversion action, then "Enhanced conversions."

You should see:
- **Eligible conversions**: Total conversions that could have enhanced data
- **Conversions with enhanced data**: How many actually got enhanced data attached
- **Enhancement rate**: Should be 65%+ if properly implemented

If your enhancement rate is under 50%, either your data capture is broken or your hashing format is wrong.

### Server-Side Verification
For the Cloud Function, check the logs:

```bash
gcloud functions logs read enhanced-conversion-webhook --limit 50
```

Look for Google Ads API errors. Common ones:
- `INVALID_CUSTOMER_USER_DATA`: Data format is wrong
- `CONVERSION_ACTION_NOT_FOUND`: Wrong conversion action ID
- `CLICK_THROUGH_NOT_FOUND`: gclid is invalid or too old (90-day limit)

### Cross-Platform Verification
Compare conversion counts between:
- Google Ads (should be highest with Enhanced Conversions)
- Google Analytics 4 (typically 10-15% lower due to client-side blocking)
- Your actual checkout system (source of truth)

Acceptable variance: Google Ads should be within 5-10% of your checkout system count. If it's off by more than 15%, something's broken.

## Troubleshooting

**Problem**: Enhancement rate is under 30%, but forms are capturing email correctly.
→ Check your hashing format. You're probably double-hashing (hashing in GTM + hashing server-side) or using the wrong algorithm. Google wants SHA-256, not MD5 or bcrypt.

**Problem**: Conversions show in Google Ads but none have enhanced data attached.
→ Your Enhanced Conversion tag isn't firing, or the data variable is returning undefined. Check GTM Preview mode and verify the Enhanced Conversion Data variable has actual values.

**Problem**: Server-side conversions aren't showing up at all.
→ Verify your gclid capture and storage. If users click an ad, browse for 10 minutes, then convert, you need to persist that gclid through their session. LocalStorage works for single-session conversions.

**Problem**: Getting "CLICK_THROUGH_NOT_FOUND" API errors.
→ gclid is either invalid, too old (>90 days), or from a different Google Ads account. Verify you're using the exact gclid from the ad click, not generating random values.

**Problem**: Enhancement rate drops after a few days of working correctly.
→ Usually means your form selectors broke due to a site update. The email/phone capture code is returning undefined. Update your CSS selectors in the GTM variable.

**Problem**: Seeing duplicate conversions in Google Ads after adding server-side tracking.
→ Google's deduplication isn't working because your conversion timestamps don't match. Use the same timestamp for both client-side and server-side events, ideally captured at the moment of conversion.

## What To Do Next

Enhanced Conversions is just one piece of a complete tracking infrastructure. Once this is working, consider these related setups:

- [Enhanced Conversions for Web Forms](/tracking/enhanced-conversions-web-forms) — capture micro-conversions for better optimization
- [Enhanced Conversions for Lead Gen](/tracking/enhanced-conversions-lead-gen) — if you're running lead generation campaigns
- [Google Ads Server-Side Tracking](/tracking/google-ads-server-side) — full server-side setup for maximum data control

Having tracking issues beyond Enhanced Conversions? I help e-commerce brands and lead gen companies audit and fix their tracking infrastructure. [Get a free tracking audit](/contact) — I'll spot-check your setup and identify the biggest gaps.

*This guide is part of the [Enhanced Conversions Setup Hub](/tracking/enhanced-conversions) — comprehensive guides for implementing Enhanced Conversions across different platforms and conversion types.*
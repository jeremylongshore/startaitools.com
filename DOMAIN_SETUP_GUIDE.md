# Custom Domain Setup Guide: startaitools.com
**Date Created: 2025-09-08**

## Overview
This guide walks you through configuring startaitools.com with Porkbun (domain registrar) and Netlify (hosting provider) for your Hugo static site.

---

## Prerequisites
- [ ] Domain purchased at Porkbun (startaitools.com)
- [ ] Netlify account created
- [ ] Hugo site ready for deployment (built successfully locally)
- [ ] Access to both Porkbun and Netlify dashboards

---

## Part 1: Deploy Your Site to Netlify First

### Step 1: Initial Netlify Deployment
1. Log in to [Netlify](https://app.netlify.com)
2. Click **"Add new site"** → **"Import an existing project"**
3. Choose your Git provider (GitHub, GitLab, or Bitbucket)
4. Select your repository containing the Hugo site
5. Configure build settings:
   - **Build command**: `hugo`
   - **Publish directory**: `public`
   - **Environment variables** (if needed):
     - `HUGO_VERSION`: (specify your Hugo version, e.g., `0.128.0`)
6. Click **"Deploy site"**
7. Wait for initial deployment (2-5 minutes)
8. Note your temporary Netlify URL (e.g., `amazing-einstein-123abc.netlify.app`)

### Step 2: Verify Deployment
1. Visit your temporary Netlify URL
2. Confirm your site loads correctly
3. Test a few pages and links
4. ✅ **Checkpoint**: Site works on Netlify subdomain

---

## Part 2: Configure Custom Domain in Netlify

### Step 3: Add Custom Domain to Netlify
1. In Netlify dashboard, go to your site
2. Navigate to **"Domain management"** (or **"Site configuration"** → **"Domain management"**)
3. Click **"Add a domain"**
4. Enter `startaitools.com`
5. Click **"Verify"**
6. Netlify will show a warning that you don't own this domain yet - click **"Add domain"** anyway
7. You'll see DNS configuration instructions - keep this page open

### Step 4: Note Netlify's Required DNS Records
Netlify will display one of two configurations:

**Option A - Using Netlify DNS (Recommended)**
- Netlify will provide 4 nameservers like:
  ```
  dns1.p01.nsone.net
  dns2.p01.nsone.net
  dns3.p01.nsone.net
  dns4.p01.nsone.net
  ```

**Option B - Using External DNS (Porkbun)**
- Netlify will provide:
  - An A record pointing to `75.2.60.5`
  - A CNAME record for www pointing to your Netlify subdomain

---

## Part 3: Configure DNS at Porkbun

### Step 5: Access Porkbun DNS Settings
1. Log in to [Porkbun](https://porkbun.com)
2. Go to **"Domain Management"**
3. Find `startaitools.com`
4. Click **"DNS"** (or the gear icon → **"DNS"**)

### Step 6A: Configuration Using Netlify DNS (Recommended)
1. In Porkbun, click **"Nameservers"** tab
2. Remove default Porkbun nameservers
3. Add Netlify's nameservers one by one:
   ```
   dns1.p01.nsone.net
   dns2.p01.nsone.net
   dns3.p01.nsone.net
   dns4.p01.nsone.net
   ```
4. Click **"Update Nameservers"**
5. ⏱️ **Wait time**: 24-48 hours for full propagation (often works within 1-4 hours)

### Step 6B: Configuration Using Porkbun DNS (Alternative)
If you prefer to keep DNS at Porkbun, add these records:

1. **Delete existing records** (if any) for @ and www
2. **Add A Record for root domain:**
   - Type: `A`
   - Host: `@` (or leave blank)
   - Answer: `75.2.60.5`
   - TTL: `600` (10 minutes during setup, increase to 86400 later)
   - Priority: Leave blank

3. **Add CNAME Record for www:**
   - Type: `CNAME`
   - Host: `www`
   - Answer: `[your-site-name].netlify.app` (your Netlify subdomain)
   - TTL: `600`
   - Priority: Leave blank

4. **Optional but recommended - Add ALIAS/ANAME record:**
   - Type: `ALIAS` (if available in Porkbun)
   - Host: `@`
   - Answer: `[your-site-name].netlify.app`
   - TTL: `600`

5. Click **"Save"** for each record
6. ⏱️ **Wait time**: 5-30 minutes for propagation

---

## Part 4: Verify DNS Configuration

### Step 7: Check DNS Propagation
1. Use [DNS Checker](https://dnschecker.org) to verify:
   - Enter `startaitools.com`
   - Check A record shows `75.2.60.5`
   - Enter `www.startaitools.com`
   - Check CNAME points to your Netlify subdomain

2. Command line verification (optional):
   ```bash
   # Check A record
   dig startaitools.com
   
   # Check CNAME
   dig www.startaitools.com
   
   # Alternative using nslookup
   nslookup startaitools.com
   nslookup www.startaitools.com
   ```

### Step 8: Verify in Netlify
1. Return to Netlify dashboard
2. Go to **"Domain management"**
3. Look for green checkmarks next to your domain
4. Status should change from "Awaiting DNS propagation" to "Netlify DNS" or "External DNS"
5. ✅ **Checkpoint**: Netlify recognizes your domain configuration

---

## Part 5: SSL Certificate Setup

### Step 9: Enable HTTPS/SSL
1. In Netlify **"Domain management"**
2. Scroll to **"HTTPS"** section
3. Click **"Verify DNS configuration"**
4. Once verified, click **"Provision certificate"**
5. Netlify uses Let's Encrypt for free SSL certificates
6. ⏱️ **Wait time**: 5-15 minutes for certificate provisioning
7. You'll see "Your site has HTTPS enabled" when complete

### Step 10: Force HTTPS (Recommended)
1. Still in the HTTPS section
2. Toggle **"Force HTTPS"** to ON
3. This redirects all HTTP traffic to HTTPS automatically

---

## Part 6: Final Configuration

### Step 11: Set Primary Domain
1. In Netlify **"Domain management"**
2. Under **"Custom domains"**
3. Click **"Options"** → **"Set as primary domain"** next to `startaitools.com`
4. This ensures `www.startaitools.com` redirects to `startaitools.com` (or vice versa)

### Step 12: Configure Redirects (Optional)
Create a `_redirects` file in your Hugo `static` folder:
```
# Redirect www to non-www
https://www.startaitools.com/* https://startaitools.com/:splat 301!

# Or redirect non-www to www (choose one)
# https://startaitools.com/* https://www.startaitools.com/:splat 301!
```

---

## Part 7: Testing & Verification

### Step 13: Comprehensive Testing
1. **Test all URL variations:**
   - [ ] http://startaitools.com (should redirect to HTTPS)
   - [ ] https://startaitools.com (should load)
   - [ ] http://www.startaitools.com (should redirect)
   - [ ] https://www.startaitools.com (should redirect to primary)

2. **Test SSL certificate:**
   - Visit https://startaitools.com
   - Click padlock icon in browser
   - Verify "Connection is secure"
   - Check certificate is issued by Let's Encrypt

3. **Test site functionality:**
   - [ ] Homepage loads
   - [ ] Navigation works
   - [ ] Images display
   - [ ] Blog posts accessible

### Step 14: DNS Performance Check
Use [Google PageSpeed Insights](https://pagespeed.web.dev/):
1. Enter `https://startaitools.com`
2. Check both mobile and desktop scores
3. Verify no DNS or SSL errors

---

## Troubleshooting Guide

### Issue: "DNS verification failed" in Netlify
**Solution:**
- Wait longer (up to 48 hours for nameserver changes)
- Verify records in Porkbun match exactly
- Clear browser cache and try again
- Try using different DNS servers (8.8.8.8 or 1.1.1.1)

### Issue: Site shows "Not Secure" warning
**Solution:**
- Ensure SSL certificate is provisioned in Netlify
- Enable "Force HTTPS" in Netlify settings
- Clear browser cache
- Wait 15 minutes and retry

### Issue: www and non-www both work but show as different sites
**Solution:**
- Set primary domain in Netlify
- Add redirect rules in `_redirects` file
- Ensure only one version is set as primary

### Issue: "404 Not Found" after domain setup
**Solution:**
- Verify build completed successfully in Netlify
- Check publish directory is set to `public`
- Ensure Hugo version matches in environment variables
- Rebuild and redeploy the site

### Issue: DNS changes not propagating
**Solution:**
- Flush local DNS cache:
  ```bash
  # Windows
  ipconfig /flushdns
  
  # macOS
  sudo dscacheutil -flushcache
  
  # Linux
  sudo systemd-resolve --flush-caches
  ```
- Try accessing from different network/device
- Use incognito/private browsing mode

---

## Expected Timeline

| Step | Expected Duration |
|------|------------------|
| Netlify initial deployment | 2-5 minutes |
| DNS record addition | Immediate |
| DNS propagation (Porkbun DNS) | 5-30 minutes |
| Nameserver propagation | 1-48 hours |
| SSL certificate provision | 5-15 minutes |
| Full global propagation | Up to 48 hours |

**Note:** Most setups work within 1-2 hours, but allow 48 hours for complete global propagation.

---

## Post-Setup Checklist

- [ ] Domain resolves correctly
- [ ] SSL certificate active
- [ ] HTTPS forced on all connections
- [ ] www redirects to non-www (or vice versa)
- [ ] Site content displays properly
- [ ] Update any hardcoded URLs in your Hugo config
- [ ] Test contact forms or dynamic features
- [ ] Set up monitoring (Netlify Analytics or Google Analytics)
- [ ] Configure custom 404 page if needed
- [ ] Test on multiple devices and browsers

---

## Additional Resources

- [Netlify DNS Documentation](https://docs.netlify.com/domains-https/custom-domains/)
- [Porkbun Help Center](https://kb.porkbun.com/)
- [Hugo Deployment Guide](https://gohugo.io/hosting-and-deployment/hosting-on-netlify/)
- [DNS Propagation Checker](https://dnschecker.org)
- [SSL Labs Test](https://www.ssllabs.com/ssltest/)

---

## Support Contacts

**Porkbun Support:**
- Email: support@porkbun.com
- Help: https://kb.porkbun.com/

**Netlify Support:**
- Community: https://answers.netlify.com/
- Documentation: https://docs.netlify.com/
- Status: https://www.netlifystatus.com/

---

**Last Updated: 2025-09-08**
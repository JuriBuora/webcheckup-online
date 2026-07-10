# Website Check-up

## Security, Trust and Visibility

**Client:** {{BUSINESS}}  
**Website analyzed:** {{URL}}  
**Date:** {{DATA}}  
**Type of check:** External, non-invasive analysis  
**Prepared by:** Juri Buora

---

## 1. Plain-language summary

{{RIEPILOGO}}

In short: I looked at the website from the outside, the way a customer or a search engine would. Below you'll find what works, what's worth improving, and in what order - without unnecessary jargon and without promising "total security" or legal compliance.

---

<!-- pagebreak -->

## 2. Priority table

| Problem | Impact | Priority | Who fixes it |
| --- | --- | --- | --- |
| {{PROBLEMA_1}} | {{IMPATTO_1}} | High | {{CHI_1}} |
| {{PROBLEMA_2}} | {{IMPATTO_2}} | Medium | {{CHI_2}} |
| {{PROBLEMA_3}} | {{IMPATTO_3}} | Low | {{CHI_3}} |

Priority legend:

- **High:** worth addressing soon, as it can reduce trust, contacts or basic functioning.
- **Medium:** useful and concrete, but not urgent.
- **Low:** a recommended improvement for when there's time.

---

## 3. Finding details

Fill in one section per relevant issue found through the checklist. Duplicate the block below for each finding.

{{FINDINGS}}

### {{TITOLO_FINDING}}

**Area:** {{AREA}} · **Priority:** {{PRIORITA}}

#### What I saw

{{COSA_VISTO}}

#### Why it matters for the business

{{PERCHE_CONTA}}

#### What to do (practical steps)

{{COSA_FARE}}

**Who can fix it:** {{CHI_SISTEMA}}

---

### Screenshots (if available)

#### Desktop

![Homepage desktop screenshot](../screenshots/homepage-desktop-viewport.png)

<!-- pagebreak -->

#### Mobile

![Homepage mobile screenshot](../screenshots/homepage-mobile-viewport.png)

<!-- pagebreak -->

---

## 4. Quick wins - 3 things fixable this week

Small but visible actions the owner or web developer can take without rebuilding the site:

1. {{QUICK_WIN_1}}
2. {{QUICK_WIN_2}}
3. {{QUICK_WIN_3}}

---

## 5. Ready-to-send message for your web developer

You can copy and send this text to whoever manages the site:

> Hi, we've had an external check-up of the website done and a few points came up worth checking. The main priorities are: {{PUNTI_WEBMASTER}}. Could you check feasibility, timing and cost to fix them?

---

<!-- pagebreak -->

## 6. Technical evidence appendix

| Evidence | Result | Source file |
| --- | --- | --- |
| Homepage HTTPS | {{EV_HTTPS}} | `homepage-headers.txt` |
| HTTP redirect | {{EV_REDIRECT}} | `http-redirect-headers.txt` |
| TLS certificate | {{EV_TLS}} | `tls-certificate.txt` |
| Hardening headers | {{EV_HEADERS}} | `homepage-headers.txt` |
| Lighthouse mobile | {{EV_LH_MOBILE}} | `lighthouse-mobile.json` |
| Lighthouse desktop | {{EV_LH_DESKTOP}} | `lighthouse-desktop.json` |
| Main links | {{EV_LINKS}} | `link-check-main.txt` |
| Visible privacy/cookies | {{EV_PRIVACY}} | `privacy-policy.html`, `cookie-policy.html` |

---

## 7. Disclaimer

Important note: this check-up is an external, non-invasive analysis of the website. It does not include penetration testing, aggressive scanning, access to restricted areas, login testing, exploits, or a full legal review. Observations on privacy/cookies do not constitute legal advice, but point out visible elements that can be checked with your own consultant or web provider.

# Guilt Eater – MVP README

### Screen Addiction Commitment App (Android Only)

> **MVP Goal:** Build a working Android app that blocks apps, tracks screen time, and enforces a money-backed commitment using Flutter + Kotlin + FastAPI + Razorpay.

---

## Scope (MVP Only)

* Android only (no iOS)
* Flutter UI
* Kotlin system services
* FastAPI backend
* PostgreSQL database
* Razorpay payments

---

## Core User Flow

* [ ] User registers
* [ ] User deposits money (Razorpay)
* [ ] User selects apps to control
* [ ] User sets daily time limits
* [ ] User grants permissions
* [ ] User starts commitment
* [ ] Violations detected
* [ ] Penalties applied
* [ ] Commitment ends
* [ ] User withdraws remaining balance

---

## Functional Requirements

### Authentication

* [ ] Email / Phone signup
* [ ] JWT authentication
* [ ] Login / Logout
* [ ] Password reset

### Wallet (Internal Ledger)

* [ ] Deposit via Razorpay Checkout
* [ ] Locked balance system
* [ ] Ledger table (all transactions)
* [ ] Withdrawal via Razorpay Payouts

### Commitment Engine

* [ ] Create commitment
* [ ] Custom duration (days)
* [ ] App-wise rules
* [ ] Daily limit per app

### Penalty Engine

* [ ] Violation counter
* [ ] Warning system (first 3)
* [ ] Percentage deduction
* [ ] Bypass detection penalties

### Android Blocking (Kotlin)

* [ ] UsageStats tracking
* [ ] Accessibility blocking overlay
* [ ] Device Admin enabled
* [ ] Boot receiver
* [ ] Safe mode detection
* [ ] Uninstall prevention

### Parent–Child Mode

* [ ] Family invite system
* [ ] Parent sets rules
* [ ] Child accepts rules
* [ ] Parent funds wallet
* [ ] Shared visibility

---

## Penalty Rules (MVP)

### Wallet Amount → Penalty Per Violation

| Amount   | Penalty |
| -------- | ------- |
| ₹50–199  | 20%     |
| ₹200–499 | 15%     |
| ₹500–999 | 10%     |
| ₹1000+   | 5%      |

### Violation Rules

| Event                     | Penalty         |
| ------------------------- | --------------- |
| 1–3 violations            | Warning only    |
| 4+ violations             | Apply penalty % |
| Uninstall attempt         | 50% penalty     |
| Permission revoke         | 50% penalty     |
| Safe mode / Factory reset | 100% penalty    |

---

## Tech Checklist

### Backend (FastAPI)

* [ ] Auth routes
* [ ] Wallet routes
* [ ] Commitment routes
* [ ] Penalty engine
* [ ] Razorpay webhooks
* [ ] PostgreSQL schema

### Android Core (Kotlin)

* [ ] UsageTrackerService
* [ ] BlockerAccessibilityService
* [ ] DeviceAdminReceiver
* [ ] BootReceiver
* [ ] Anti-tamper logic

### Flutter UI

* [ ] Login / Signup screen
* [ ] Wallet screen
* [ ] Commitment setup screen
* [ ] Permissions screen
* [ ] Violation history screen
* [ ] Withdrawal screen

---

## Payment Flow (MVP)

* [ ] Razorpay Checkout → Deposit
* [ ] Webhook → Confirm payment
* [ ] Ledger update
* [ ] Penalties → Deduct locked balance
* [ ] Withdrawal → Razorpay Payout

---

## Definition of Done

* [ ] Instagram blocked when limit exceeded
* [ ] Money deducted after violations
* [ ] Uninstall triggers penalty
* [ ] Withdrawal works
* [ ] Parent–child mode works

---

## Non‑Goals (Out of MVP)

* iOS support
* AI coach
* Rewards / points
* Social features
* Leaderboards

---

**This README is the execution checklist for the Guilt Eater MVP.**

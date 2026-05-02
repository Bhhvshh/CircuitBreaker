# CircuitBreaker

A simple demonstration of the **Circuit Breaker** design pattern using Python, Flask, and [pybreaker](https://github.com/danielfm/pybreaker).

## Overview

This project simulates a microservices architecture with two services:

- **Order Service** (`order.py`) — receives order requests and calls the Payment Service. It wraps the payment call with a circuit breaker to handle failures gracefully.
- **Payment Service** (`payment.py`) — simulates an unstable payment backend with a 50% random failure rate and variable response delays.

### How the Circuit Breaker Works

| State | Description |
|-------|-------------|
| **Closed** | Requests flow normally to the Payment Service. |
| **Open** | After 3 consecutive failures, the circuit opens and requests are blocked immediately (fast-fail) for 10 seconds. |
| **Half-Open** | After the timeout, one request is allowed through to test if the service has recovered. |

## Prerequisites

- Python 3.7+
- pip

## Installation

```bash
pip install flask requests pybreaker
```

## Running the Project

Open two terminal windows and start each service separately.

**Terminal 1 – Start the Payment Service (port 5001):**
```bash
python payment.py
```

**Terminal 2 – Start the Order Service (port 5000):**
```bash
python order.py
```

## Usage

Place an order by calling the Order Service:

```bash
curl http://localhost:5000/order
```

**Successful response:**
```json
{
  "status": "success",
  "payment_response": {"message": "Payment processed successfully"}
}
```

**Response when circuit is open (service unavailable):**
```json
{
  "status": "error",
  "message": "⚠️ Payment Service unavailable (circuit open). Please try later."
}
```

## Circuit Breaker Configuration

Configured in `order.py`:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `fail_max` | `3` | Number of consecutive failures before opening the circuit |
| `reset_timeout` | `10` | Seconds to wait before attempting recovery (half-open state) |

## Project Structure

```
CircuitBreaker/
├── order.py      # Order Service with circuit breaker logic
├── payment.py    # Payment Service (simulates failures)
└── README.md
```

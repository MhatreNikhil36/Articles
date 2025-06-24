

### ✅ **Clarification: What Is a Cumulative Join in SCD Type 2?**

In **SCD Type 2 dimension building**, the term *cumulative join* is sometimes used **in two different contexts**:

---

#### **Context A: Cumulative Join for Matching Facts to Historical Dimensions**

where we join a **fact table** to an SCD2 dimension based on time intervals (e.g., `event_time BETWEEN effective_start AND effective_end`).

✅ **Used in data marts or reporting layers**
❌ **Not how you *build* the SCD table**

---

#### **Context B: Cumulative Join for Building SCD Type 2 from Change Data**

when *building* the SCD2 table from a staging or raw delta feed (today’s and yesterday’s snapshot), a **self join (aka cumulative or change join)** is performed between:

* **today's snapshot (`today`)**
* **yesterday's SCD state (`yesterday`)**

To **detect changes**, **close old rows**, and **open new rows**.

---

## ✅ Let's Write the Correct General SQL `README.md` for This Case

Here's a refined version that works for **PostgreSQL**, **MySQL (with some notes)**, and other general RDBMS — explaining **how to build SCD Type 2 using a cumulative join** pattern.

---

# 📘 SCD Type 2 with Cumulative Join (PostgreSQL-Compatible SQL)

This article explains how to implement **Slowly Changing Dimension Type 2 (SCD2)** using a **cumulative join** between current and prior snapshots of a dimension.

---

## ✅ What Is This?

A **cumulative join** in this context is a **self-join between two snapshots** of the same dataset (e.g., yesterday’s and today’s customer dimension) to detect changes in records.

This technique lets you:

* Detect new rows
* Detect changed values
* Generate new `effective_start` and `effective_end` dates
* Maintain **full historical audit trail**

---

## 📌 Use Case

You're loading a `customer` dimension table from a daily snapshot (or CDC feed) and need to track historical changes like:

* Name change
* Status update
* Any attribute modification

Each time a change is detected, a **new row** is created with a new `effective_start` and an open-ended `effective_end`.

---

## 🧪 Sample Input

### Snapshot from **yesterday** (`dim_customer_yesterday`):

| customer\_id | name  | status | effective\_start | effective\_end |
| ------------ | ----- | ------ | ---------------- | -------------- |
| 101          | Alice | Bronze | 2020-01-01       | 9999-12-31     |

### Snapshot from **today** (`customer_staging`):

| customer\_id | name  | status |
| ------------ | ----- | ------ |
| 101          | Alice | Silver |
| 102          | Bob   | Bronze |

---

## 🔄 Step-by-Step Logic

### Step 1: Identify Changed Rows

```sql
SELECT s.*
FROM customer_staging s
LEFT JOIN dim_customer_yesterday y
  ON s.customer_id = y.customer_id
WHERE y.customer_id IS NULL  -- new customer
   OR s.name IS DISTINCT FROM y.name
   OR s.status IS DISTINCT FROM y.status;
```

> ✅ `IS DISTINCT FROM` works even if NULLs are involved (PostgreSQL only).
> In MySQL, use: `s.name <> y.name OR (s.name IS NULL AND y.name IS NOT NULL) OR ...`

---

### Step 2: Expire Old Rows

```sql
UPDATE dim_customer
SET effective_end = CURRENT_DATE - INTERVAL '1 day'
WHERE customer_id IN (
  SELECT s.customer_id
  FROM customer_staging s
  JOIN dim_customer y ON s.customer_id = y.customer_id
  WHERE s.name IS DISTINCT FROM y.name
     OR s.status IS DISTINCT FROM y.status
)
AND effective_end = '9999-12-31';
```

---

### Step 3: Insert New Rows

```sql
INSERT INTO dim_customer (
  customer_id,
  name,
  status,
  effective_start,
  effective_end
)
SELECT
  s.customer_id,
  s.name,
  s.status,
  CURRENT_DATE,
  '9999-12-31'
FROM customer_staging s
LEFT JOIN dim_customer y
  ON s.customer_id = y.customer_id
WHERE y.customer_id IS NULL
   OR s.name IS DISTINCT FROM y.name
   OR s.status IS DISTINCT FROM y.status;
```

---

## 🧠 Key Considerations

| Concept                 | Detail                                                      |
| ----------------------- | ----------------------------------------------------------- |
| 🔁 Join Granularity     | Always join on `business_key`, never on surrogate PK        |
| 🕰 Sentinel Dates       | Use `9999-12-31` or another sentinel for open rows          |
| 💡 Null-Safe Comparison | Prefer `IS DISTINCT FROM` to handle NULLs safely            |
| 🧼 De-duplication       | Use window functions if your source snapshot has duplicates |
| ⚡ Performance           | Consider indexing `customer_id, effective_end`              |
| 🧪 Testing              | Cover all edge cases: new, updated, unchanged, deleted      |

---

## ✅ Example Table Setup (PostgreSQL-Compatible)

```sql
-- Historical table
CREATE TABLE dim_customer (
  customer_id INT,
  name TEXT,
  status TEXT,
  effective_start DATE,
  effective_end DATE
);

-- Incoming snapshot
CREATE TABLE customer_staging (
  customer_id INT,
  name TEXT,
  status TEXT
);
```

---

## 🧪 Suggested Test Cases

| Scenario                       | Expected Outcome                      |
| ------------------------------ | ------------------------------------- |
| New customer in staging        | Insert with current\_date start       |
| Customer exists with no change | No insert/update                      |
| Attribute changed              | Expire old row, insert new one        |
| Nulls introduced or removed    | Handled safely using null-aware logic |

---

## ❌ When Not to Use This Pattern

* You don't care about **history** (use SCD Type 1 instead)
* Changes come in real-time (prefer event-driven CDC)
* Source system lacks reliable unique IDs (joins won’t work safely)

---

## 📎 Example Repo

> You can explore this in the [`SCD2_CumulativeJoin`](./SCD2_CumulativeJoin) folder of this repo.

Includes:

* Full SQL scripts
* Sample data setup
* Queries to test SCD2 logic manually

---

## 👨‍💻 Author

**Nikhil Mhatre**
📎 [Portfolio](https://mhatrenikhil36.github.io/me/) • [GitHub](https://github.com/MhatreNikhil36) • [LinkedIn](https://linkedin.com/in/nikhil-nandkumar-mhatre)


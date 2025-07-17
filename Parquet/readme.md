
# Apache Parquet: Quick Reference Guide

**Apache Parquet** is an open-source, columnar data storage format built for fast analytics and scalable big data pipelines.

---

## 📂 Parquet File Structure

![Parquet file internal structure](https://media.datacamp.com/cms/ad_4nxcuuincavq5rqwc42rsxrqtf_hrepxa5zaohmvbkyjdivivu2p79s8pkbiov5ws85byacezrthjzpkg_uk-b1gybmog8fszuf_edkdle1j36eixnmhqb7unprq4emw4phm__zrp.png)

* **Footer (Metadata)**: Schema, statistics, row group index
* **Row Groups**: Batch of rows, split into columns
* **Column Chunks**: Data for each column (enables fast, selective reads)
* **Pages**: Each chunk split for compression/efficiency

---

## ⭐ Key Features

* **Columnar Storage**: Read only the columns you need
* **Compression**: Snappy (fast), Gzip (compact), Brotli
* **Efficient Encoding**: Run-length, dictionary encoding
* **Schema Evolution**: Add/remove/rename columns without breaking reads
* **Predicate Pushdown**: Filter data at read time for speed
* **Rich Metadata**: File footer holds all schema/stats info

---

## 🔧 Read & Write Parquet

### With Pandas

```python
import pandas as pd
df = pd.DataFrame({...})
df.to_parquet("file.parquet", engine="pyarrow")         # Write
df = pd.read_parquet("file.parquet", engine="pyarrow")  # Read
```

### With PyArrow

```python
import pyarrow as pa, pyarrow.parquet as pq
table = pa.Table.from_pandas(df)
pq.write_table(table, "file.parquet")
table = pq.read_table("file.parquet")
df = table.to_pandas()
```

### With PySpark

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Parquet").getOrCreate()
df = spark.createDataFrame(data, schema)
df.write.parquet("file.parquet")
df = spark.read.parquet("file.parquet")
```

---

## 🛠️ Common Operations

* **Append Data**: Read, concatenate, write back with PyArrow.
* **Read Specific Columns**:
  `pd.read_parquet("file.parquet", columns=["col1"])`
* **Filter Rows at Read**:
  `pq.read_table("file.parquet", filters=[("Age", ">", 30)])`
* **Partition Data**:
  `df.to_parquet("out/", partition_cols=["City"])`
* **Merge Files**: Concatenate, write as new file.
* **CSV to Parquet**:
  `pd.read_csv("file.csv").to_parquet("file.parquet")`

---

## 💡 Best Practices

* **Snappy for speed, Gzip for storage.**
* **Partition by high-cardinality fields** for query speed.
* **Add columns, avoid disruptive schema changes.**
* **Batch writes** to avoid too many small files.

---

## 📊 Parquet vs. Other Formats

| Format  | Pros                                     | Cons                         | Use Cases           |
| ------- | ---------------------------------------- | ---------------------------- | ------------------- |
| Parquet | Fast analytics, compresses well, schema  | Not human-readable, complex  | Data lakes, OLAP    |
| CSV     | Simple, readable                         | No schema, slow for big data | Interchange, legacy |
| JSON    | Flexible, semi-structured                | Large, slow for analytics    | APIs, logs          |
| Avro    | Fast writes, row-based, schema evolution | Not for analytics            | Streaming, Kafka    |

---

## 🚦 When to Use Parquet

* Analytics & OLAP workloads
* Data lakes on S3, GCS, Azure
* Large, evolving datasets
* Columnar query needs

---

## 📚 Learn More

* [Original DataCamp Parquet Article](https://www.datacamp.com/tutorial/apache-parquet)
* [Apache Parquet Official Docs](https://parquet.apache.org/documentation/latest/)
* [PyArrow Documentation](https://arrow.apache.org/docs/python/parquet.html)
* [Spark SQL Guide on Parquet](https://spark.apache.org/docs/latest/sql-data-sources-parquet.html)
* [AWS Athena and Parquet](https://docs.aws.amazon.com/athena/latest/ug/parquet.html)

---

*Image credit: DataCamp, see original article for more diagrams and explanation.*

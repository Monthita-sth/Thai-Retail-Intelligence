from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("ThaiRetailTest")
        .master("local[*]")
        .getOrCreate()
    )

    print("Spark version:", spark.version)

    data = [
        (1, "Bangkok", 1200),
        (2, "Chiang Mai", 800),
        (3, "Phuket", 1500),
    ]

    df = spark.createDataFrame(
        data,
        ["order_id", "province", "revenue"]
    )

    df.show()

    spark.stop()


if __name__ == "__main__":
    main()
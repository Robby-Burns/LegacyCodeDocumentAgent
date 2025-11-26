CREATE PROCEDURE [dbo].[sp_GenerateMonthlyRevenue]
    @StartDate DATETIME,
    @EndDate DATETIME
AS
    BEGIN
    SET
    NOCOUNT ON;

    -- CTE to handle currency conversion rates based on transaction date
    WITH CurrencyRates AS (SELECT FromCurrency,
                                  ToCurrency,
                                  Rate,
                                  EffectiveDate,
                                  LEAD(EffectiveDate) OVER (PARTITION BY FromCurrency, ToCurrency ORDER BY EffectiveDate) as NextRateDate
                           FROM Finance.ExchangeRates),

         -- Aggregate base sales excluding soft-deleted items
         RawSales AS (SELECT t.OrderID,
                             t.CustomerID,
                             t.TransactionDate,
                             t.Amount,
                             t.CurrencyCode,
                             CASE
                                 WHEN t.TypeID = 1 THEN 'Subscription'
                                 WHEN t.TypeID = 2 THEN 'OneTime'
                                 WHEN t.TypeID = 3 AND t.Amount < 0 THEN 'Refund'
                                 ELSE 'Misc'
                                 END as RevenueType
                      FROM Sales.Transactions t
                      WHERE t.IsDeleted = 0
                        AND t.TransactionDate BETWEEN @StartDate AND @EndDate)

    -- Final Report Join
    SELECT FORMAT(rs.TransactionDate, 'yyyy-MM') as MonthPeriod,
           rs.RevenueType,
           c.Region,
           COUNT(DISTINCT rs.CustomerID)         as UniqueCustomers,
           SUM(
                   CASE
                       WHEN rs.CurrencyCode = 'USD' THEN rs.Amount
                       ELSE rs.Amount * cr.Rate
                       END
           )                                     as TotalAmountUSD,
           SUM(
                   CASE
                       WHEN rs.RevenueType = 'Refund' THEN 1
                       ELSE 0
                       END
           )                                     as RefundCount
    FROM RawSales rs
             LEFT JOIN Customers.Profiles c ON rs.CustomerID = c.ID
             LEFT JOIN CurrencyRates cr
                       ON rs.CurrencyCode = cr.FromCurrency
                           AND cr.ToCurrency = 'USD'
                           AND rs.TransactionDate >= cr.EffectiveDate
                           AND (rs.TransactionDate < cr.NextRateDate OR cr.NextRateDate IS NULL)
    GROUP BY FORMAT(rs.TransactionDate, 'yyyy-MM'),
             rs.RevenueType,
             c.Region
    HAVING SUM(rs.Amount) > 0
    ORDER BY MonthPeriod DESC;
    END
                                  
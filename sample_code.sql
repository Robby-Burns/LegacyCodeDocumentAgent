CREATE PROCEDURE GetDelinquentLoans
    @DaysOverdue INT = 30,
    @LoanType VARCHAR(20) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        m.MemberID,
        m.FirstName + ' ' + m.LastName AS MemberName,
        l.LoanID,
        l.LoanType,
        l.OriginalAmount,
        l.CurrentBalance,
        l.PaymentDueDate,
        DATEDIFF(DAY, l.PaymentDueDate, GETDATE()) AS DaysDelinquent,
        l.InterestRate,
        la.AccountStatus
    FROM Members m
    INNER JOIN Loans l ON m.MemberID = l.MemberID
    INNER JOIN LoanAccounts la ON l.LoanID = la.LoanID
    WHERE
        l.PaymentDueDate < DATEADD(DAY, -@DaysOverdue, GETDATE())
        AND la.AccountStatus = 'Active'
        AND (@LoanType IS NULL OR l.LoanType = @LoanType)
    ORDER BY DaysDelinquent DESC;
END
CREATE PROCEDURE GetMemberByID
    @MemberID INT
AS
BEGIN
    SELECT
        MemberID,
        FirstName,
        LastName,
        Email,
        Phone,
        DateJoined,
        MembershipStatus
    FROM Members
    WHERE MemberID = @MemberID;
END
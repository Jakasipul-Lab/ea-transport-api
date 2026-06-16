// file: ticketModel.js
// Blueprint for the secure EA Safari Routes digital ticket payload

const createTicketPayload = (passengerName, routeFrom, routeTo, travelDate, seatInfo, baseFare, officialRef) => {
    const commissionRate = 0.05; // 5% modern services commission
    const commissionAmount = baseFare * commissionRate;
    const totalPaid = baseFare + commissionAmount;

    return {
        issuer: "ea-safari-routes",
        headOffice: "Kisumu, Kenya",
        agencyTransactionId: "SR-" + Math.floor(100000 + Math.random() * 900000),
        officialOperatorRef: officialRef, // Holds the true TRC or KRC reference code
        passenger: passengerName,
        trip: {
            from: routeFrom,
            to: routeTo,
            date: travelDate,
            seat: seatInfo
        },
        financials: {
            baseFare: baseFare,
            agencyCommission: commissionAmount,
            totalCharged: totalPaid
        },
        timestamp: new Date().toISOString()
    };
};

module.exports = { createTicketPayload };
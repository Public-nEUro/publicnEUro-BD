import { UserInfoWithoutTimestamp } from "@services/usage-client";

export const getUsernameAndTicketId = (
    userInfo: UserInfoWithoutTimestamp | undefined
): { changed_by: string; ticket_id: string } | null => {
    const username = userInfo?.username;
    if (!username) {
        alert("You don't have a username");
        return null;
    }
    const ticketId = prompt("Ticket ID");
    if (ticketId == null) return null;
    if (!ticketId) {
        alert("You need to specify a ticket ID");
        return null;
    }
    return { changed_by: username, ticket_id: ticketId };
};

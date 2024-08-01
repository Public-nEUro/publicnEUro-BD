import { DefaultService, Group, User } from "@services/usage-client";
import { firstValueFrom } from "rxjs";

const waitForJobToComplete = (service: DefaultService, jobId: string): Promise<void> =>
    new Promise((resolve, reject) => {
        const interval = window.setInterval(() => {
            service.getJobStatusPost({ job_id: jobId }).subscribe(res => {
                if (res.status === "PENDING") return;
                window.clearInterval(interval);
                if (res.status === "COMPLETED") {
                    resolve();
                    return;
                }
                if (res.status === "FAILED") alert("Something went wrong: " + res.logs);
                else alert(`Unknown status: ${res.status}`);
                reject();
            });
        }, 1000);
    });

export type UserWithRoles = { info: User; role_ids: string[] };

export type GroupWithUsersInput = {
    ticket_id: string;
    group: Group;
    hpc_owner: User;
    users: UserWithRoles[];
};

export const addGroupWithUsers = async (service: DefaultService, input: GroupWithUsersInput) => {
    const res = await firstValueFrom(service.getUserInfoPost({}));
    const username = res.auth_info.username;
    console.log("Adding group...");
    const addGroupResponse = await firstValueFrom(
        service.addGroupPost({
            group: input.group,
            user: input.hpc_owner,
            ticket_id: input.ticket_id,
            changed_by: username
        })
    );
    if (!addGroupResponse.job_id) {
        alert(addGroupResponse.error_message);
        return;
    }
    try {
        console.log("Waiting for job to complete...");
        await waitForJobToComplete(service, addGroupResponse.job_id);
    } catch {
        return;
    }
    console.log("Adding users...");
    for (let user of input.users) {
        const addUserResponse = await firstValueFrom(
            service.addUserPost({
                ...user.info,
                group_name: input.group.group_name,
                ticket_id: input.ticket_id,
                changed_by: username
            })
        );
        if (!addUserResponse.job_id) {
            console.log(addUserResponse.error_message);
            continue;
        }
        try {
            console.log("Waiting for job to complete...");
            await waitForJobToComplete(service, addUserResponse.job_id);
        } catch {}
    }
    console.log("Adding roles...");
    for (let user of input.users) {
        for (let role_id of user.role_ids) {
            const addMemberResponse = await firstValueFrom(
                service.addMemberPost({
                    group_name: input.group.group_name,
                    username: user.info.username,
                    role_id,
                    ticket_id: input.ticket_id,
                    changed_by: username
                })
            );
            if (!addMemberResponse.job_id) continue;
            try {
                console.log("Waiting for job to complete...");
                await waitForJobToComplete(service, addMemberResponse.job_id);
            } catch {}
        }
    }
    alert("Done");
};

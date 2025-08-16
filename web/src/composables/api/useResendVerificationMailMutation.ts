import { useMutation } from "@tanstack/vue-query";
import { toast } from "vue-sonner";
import { postApiMeResendVerification } from "@/services/api/me/resend-verification.ts";


export function useResendVerificationMailMutation() {
    return useMutation({
        mutationFn: async () => {
            const toastId = toast.loading("Requesting Verification Mail...");
            try {
                await postApiMeResendVerification();

                toast.success("Verification Mail was re-sent", {
                    id: toastId,
                });
            } catch (error) {
                console.log(error);
                toast.error("Failed to re-send verification mail", {
                    id: toastId,
                    description: `${error}`,
                });
            }
        },
    });
}

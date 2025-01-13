import { AbstractControl, ValidationErrors, ValidatorFn } from "@angular/forms";
import * as zxcvbn from "zxcvbn";

export const passwordStrengthNames = ["Very Weak", "Weak", "Fair", "Good", "Strong"] as const;

export const passwordStrengthValidator =
    (self: { passwordStrength: string }): ValidatorFn =>
    ({ value }) => {
        const strength = zxcvbn(value).score; // Between 0 and 4
        self.passwordStrength = passwordStrengthNames[strength];
        if (strength < 3) return { tooWeak: true };
        return null;
    };

export const matchFields =
    (fieldKey: string, repeatFieldKey: string): ValidatorFn =>
    (group: AbstractControl): ValidationErrors | null => {
        const value = group.get(fieldKey)?.value;
        const repeatValue = group.get(repeatFieldKey)?.value;
        const error = value === repeatValue ? null : { repeatMismatch: true };
        group.get(repeatFieldKey)?.setErrors(error);
        return error;
    };

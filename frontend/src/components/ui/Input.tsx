import { InputHTMLAttributes } from "react";
import { colors } from "../../design";

type Props = InputHTMLAttributes<HTMLInputElement>;

export default function Input(props: Props) {

    return (

        <input
            {...props}
            style={{
                width: "100%",
                height: 40,
                padding: "0 14px",
                borderRadius: 8,
                border: `1px solid ${colors.border}`,
                outline: "none",
                background: colors.surface,
                ...props.style,
            }}
        />

    );

}

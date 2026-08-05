import { ButtonHTMLAttributes } from "react";
import { colors } from "../../design";

type Props = ButtonHTMLAttributes<HTMLButtonElement>;

export default function Button(props: Props) {

    return (

        <button
            {...props}
            style={{
                height: 36,
                padding: "0 14px",
                borderRadius: 8,
                border: "none",
                cursor: "pointer",
                background: colors.primary,
                color: "#fff",
                fontWeight: 600,
                ...props.style,
            }}
        />

    );

}

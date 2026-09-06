import type { ReactNode } from "react";
export default function Card({
  children,
  className,
  animated = false,
}: {
  children: ReactNode;
  className?: string;
  animated?: boolean;
}) {
  return (
    <section
      className={["card", className, animated && "card-interactive"]
        .filter(Boolean)
        .join(" ")}
    >
      {children}
    </section>
  );
}

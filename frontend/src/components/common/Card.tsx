import { motion } from "framer-motion";
import type { ReactNode } from "react";

type CardProps = {
  children: ReactNode;
  className?: string;
  animated?: boolean;
};

function Card({ children, className, animated = false }: CardProps) {
  const classes = ["card", className].filter(Boolean).join(" ");

  if (animated) {
    return (
      <motion.section
        className={classes}
        whileHover={{ y: -4 }}
        transition={{ type: "spring", stiffness: 300, damping: 20 }}
      >
        {children}
      </motion.section>
    );
  }

  return <section className={classes}>{children}</section>;
}

export default Card;

type PageHeaderProps = {
  title: string;
  subtitle?: string;
};

function PageHeader({ title, subtitle = "Coming Soon" }: PageHeaderProps) {
  return (
    <header className="page-header">
      <h1>{title}</h1>
      {subtitle && <p>{subtitle}</p>}
    </header>
  );
}

export default PageHeader;

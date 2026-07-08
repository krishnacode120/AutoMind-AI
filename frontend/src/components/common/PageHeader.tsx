type PageHeaderProps = {
  title: string;
};

function PageHeader({ title }: PageHeaderProps) {
  return (
    <header className="page-header">
      <h1>{title}</h1>
      <p>Coming Soon</p>
    </header>
  );
}

export default PageHeader;

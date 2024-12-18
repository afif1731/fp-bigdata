import Head from 'next/head'

type LayoutProps = {
  children: React.ReactNode
  title?: string
}

export default function Layout({
  children,
  title = 'default title',
}: LayoutProps) {

  return (
    <div>
      <Head>
        <title>{`${title} | Based Hospital`}</title>
        <link rel='shortcut icon' href='/images/favicon.ico' />
        <meta charSet='utf-8' />
        <meta name='viewport' content='initial-scale=1.0, width=device-width' />
        <meta lang='id'/>
      </Head>
      {children}
    </div>
  )
}

import './globals.css'
import { Providers } from './providers'

export const metadata = {
  title: 'OSARE \u2014 East Africa Safari Routes & Transit Hub',
  description: 'Free information assistant & booking hub for tourists and locals across East Africa. Safaris, Kilimanjaro, hotels, car hire, flights & Nairobi transit.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <script dangerouslySetInnerHTML={{__html:'window.addEventListener("error",function(e){if(e.error instanceof DOMException&&e.error.name==="DataCloneError"&&e.message&&e.message.includes("PerformanceServerTiming")){e.stopImmediatePropagation();e.preventDefault()}},true);'}} />
      </head>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}

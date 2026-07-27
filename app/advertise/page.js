import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-blue-500 text-white">
      <div className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl md:text-6xl font-extrabold mb-3 drop-shadow-lg">OSARE</h1>
        <p className="text-xl opacity-95 mb-12">East Africa Safari & Commuter Routes</p>

        <div className="flex gap-8 justify-center flex-wrap">
          {/* Card 1: EAsafari */}
          <CardLink 
            href="/easafari"
            icon="🚄"
            title="EAsafari Routes"
            desc="Long-distance travel: SGR, Buses & Intercity options"
          />
          {/* Card 2: Jakasipul */}
          <CardLink 
            href="/jakasipul"
            icon="🚌"
            title="Jakasipul Hub"
            desc="Matatu, Local Routes & Commuter Transport"
          />
        </div>

        <div className="mt-16">
          <Link href="/advertise" className="underline opacity-90 hover:opacity-100">
            Are you a vendor? Advertise with us
          </Link>
        </div>

        <footer className="mt-20 opacity-90 text-sm">
          <p>© 2026 Osare • Aggregating Kenya's Transport Network</p>
          <p className="mt-2 font-semibold">Osare is here to serve you</p>
        </footer>
      </div>
    </div>
  )
}

function CardLink({ href, icon, title, desc }) {
  return (
    <Link href={href} className="bg-white/10 backdrop-blur-md border-white/20 rounded-2xl p-10 w-96 hover:-translate-y-2 transition text-left">
      <div className="text-4xl mb-4">{icon}</div>
      <h2 className="text-2xl font-bold mb-3">{title}</h2>
      <p className="opacity-90 mb-6">{desc}</p>
      <span className="inline-block px-6 py-3 bg-white text-blue-800 font-semibold rounded-full">
        Go to {title}
      </span>
    </Link>
  )
}

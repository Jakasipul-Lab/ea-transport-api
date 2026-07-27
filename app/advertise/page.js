import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Bus, Train } from "lucide-react"

export default function HomePage() {
  return (
    <main className="container mx-auto px-4 py-16">
      <section className="text-center mb-16">
        <h1 className="text-5xl md:text-6xl font-extrabold mb-3">OSARE</h1>
        <p className="text-xl text-muted-foreground">East Africa Safari & Commuter Routes</p>
      </section>

      <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        <Link href="/easafari">
          <Card className="hover:shadow-lg transition hover:-translate-y-1 cursor-pointer h-full">
            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-2xl">
                <Train className="w-8 h-8 text-blue-600"/> EAsafari Routes
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Long-distance travel: SGR, Buses & Intercity options</p>
            </CardContent>
          </Card>
        </Link>

        <Link href="/jakasipul">
          <Card className="hover:shadow-lg transition hover:-translate-y-1 cursor-pointer h-full">
            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-2xl">
                <Bus className="w-8 h-8 text-blue-600"/> Jakasipul Hub
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Matatu, Local Routes & Commuter Transport</p>
            </CardContent>
          </Card>
        </Link>
      </div>

      <div className="text-center mt-12">
        <Link href="/advertise" className="text-sm underline text-muted-foreground hover:text-foreground">
          Are you a vendor? Advertise with us
        </Link>
      </div>
    </main>
  )
}

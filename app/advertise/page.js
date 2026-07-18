import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Check, Handshake, Megaphone, TrendingUp } from "lucide-react"
import Link from "next/link"

const COMMISSION_RATE = 0.05 // matches your API

export default function AdvertisePage() {
  const whatsappNumber = "+254758378729"
  const whatsappMsg = encodeURIComponent("Hi OSARE, I want to advertise my safari/transport business")
  const whatsappUrl = `https://wa.me/${whatsappNumber.replace(/[^0-9]/g, "")}?text=${whatsappMsg}`

  return (
    <main className="container mx-auto px-4 py-12">
      {/* Hero */}
      <section className="text-center mb-16">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">Advertise With Us</h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-6">
          Reach tourists and daily commuters across East Africa. Free for travelers. Pay only on results for vendors.
        </p>
        <Button asChild size="lg">
          <Link href={whatsappUrl} target="_blank">Partner With Us on WhatsApp</Link>
        </Button>
      </section>

      {/* Why Us */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold mb-6 text-center">Why Advertise on OSARE</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <Card>
            <CardHeader><CardTitle className="flex items-center gap-2"><Megaphone className="w-5 h-5"/> Daily Commuters</CardTitle></CardHeader>
            <CardContent>Locals use us daily for matatus, buses, and shuttles. Get featured on high-traffic route pages.</CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="flex items-center gap-2"><TrendingUp className="w-5 h-5"/> Safari Travelers</CardTitle></CardHeader>
            <CardContent>Tourists find safari vendors through our free guides. We send them straight to your WhatsApp.</CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="flex items-center gap-2"><Handshake className="w-5 h-5"/> Pay Only on Results</CardTitle></CardHeader>
            <CardContent>${COMMISSION_RATE * 100}% commission on confirmed bookings only. $0 upfront. No ads spend risk.</CardContent>
          </Card>
        </div>
      </section>

      {/* How it works */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold mb-6 text-center">How the {COMMISSION_RATE * 100}% Safari Referral Works</h2>
        <div className="grid md:grid-cols-4 gap-4 text-center">
          {[
            "1. List Your Service", 
            "2. We Feature You in Guides", 
            "3. Tourist Books via WhatsApp", 
            "4. You Pay 5% After Booking"
          ].map((step, i) => (
            <Card key={i}>
              <CardContent className="pt-6">
                <Check className="w-8 h-8 mx-auto mb-2 text-green-500"/>
                <p className="font-medium">{step}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="text-center bg-muted rounded-2xl p-8">
        <h2 className="text-2xl font-bold mb-2">Ready to get bookings?</h2>
        <p className="text-muted-foreground mb-4">Join transport companies and safari vendors already on OSARE</p>
        <Button asChild>
          <Link href={whatsappUrl} target="_blank">Chat on WhatsApp: {whatsappNumber}</Link>
        </Button>
      </section>
    </main>
  )
}

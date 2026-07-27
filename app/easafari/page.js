import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, HelpCircle } from "lucide-react"

export default function EAsafariPage() {
  return (
    <main className="container mx-auto px-4 py-12">
      <Link href="/" className="flex items-center gap-2 text-sm mb-6 hover:underline">
        <ArrowLeft className="w-4 h-4"/> Back to Home
      </Link>
      
      <h1 className="text-4xl font-bold mb-2">🚄 EAsafari Routes</h1>
      <p className="text-muted-foreground mb-6">Your gateway to comfortable long-distance travel across East Africa.</p>

      <p className="mb-8">
        We’re here to serve you better. Find schedules, operators, and route information all in one place. 
        Need assistance? <Link href="/help" className="underline font-medium">Visit our Help Page</Link>
      </p>
      
      <Card>
        <CardHeader><CardTitle>Popular Long-Distance Routes</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <p>• Nairobi ↔ Mombasa - SGR & Highway Buses</p>
          <p>• Nairobi ↔ Kisumu - VIP Buses</p>
          <p>• Nairobi ↔ Eldoret - Shuttle & Bus</p>
          <p>• Nairobi ↔ Kampala - Cross-border Coaches</p>
        </CardContent>
      </Card>
    </main>
  )
}

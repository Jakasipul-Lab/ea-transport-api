
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, HelpCircle } from "lucide-react"

export default function JakasipulPage() {
  return (
    <main className="container mx-auto px-4 py-12">
      <Link href="/" className="flex items-center gap-2 text-sm mb-6 hover:underline">
        <ArrowLeft className="w-4 h-4"/> Back to Home
      </Link>
      
      <h1 className="text-4xl font-bold mb-2">🚌 Jakasipul Hub</h1>
      <p className="text-muted-foreground mb-6">Reliable local transport for your daily commute.</p>

      <p className="mb-8">
        We’re here to serve you better. Discover matatu routes, terminals, and commuter tips. 
        For support, <Link href="/help" className="underline font-medium">visit our Help Page</Link>
      </p>
      
      <Card>
        <CardHeader><CardTitle>Major Terminals & Routes</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <p>• Nairobi: Githurai, Dandora, Rongai, Ngong, Kasarani</p>
          <p>• Mombasa: Likoni, Nyali, Bamburi, Changamwe</p>
          <p>• Kisumu: Kibuye, Nyanza, Kondele</p>
          <p>• Eldoret: Langas, Huruma, Pioneer</p>
        </CardContent>
      </Card>
    </main>
  )
}

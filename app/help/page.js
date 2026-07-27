import Link from "next/link"
import { ArrowLeft } from "lucide-react"

export default function HelpPage() {
  return (
    <main className="container mx-auto px-4 py-12 max-w-2xl">
      <Link href="/" className="flex items-center gap-2 text-sm mb-6 hover:underline">
        <ArrowLeft className="w-4 h-4"/> Back to Home
      </Link>
      <h1 className="text-3xl font-bold mb-4">Help & Support</h1>
      <p className="text-muted-foreground mb-6">
        We’re committed to making your travel planning easier. 
        For route inquiries, vendor support, or feedback, please reach out.
      </p>
      <div className="space-y-2">
        <p><b>Email:</b> support@osare.co.ke</p>
        <p><b>Hours:</b> Mon - Sat, 8AM - 6PM EAT</p>
      </div>
    </main>
  )
}

"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import { ArrowLeft, Info, Copy, Check } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import JsBarcode from "jsbarcode"

export default function GCashCashIn() {
  const [amount, setAmount] = useState("")
  const [step, setStep] = useState<"input" | "barcode">("input")
  const [barcodeData, setBarcodeData] = useState<{
    code: string
    referenceCode: string
    expiryDate: string
  } | null>(null)
  const [copied, setCopied] = useState(false)
  const [error, setError] = useState("")
  const barcodeRef = useRef<SVGSVGElement>(null)

  const formatAmount = (value: string) => {
    // Remove non-numeric characters except decimal point
    const numericValue = value.replace(/[^\d.]/g, "")

    // Ensure only one decimal point
    const parts = numericValue.split(".")
    if (parts.length > 2) {
      return parts[0] + "." + parts.slice(1).join("")
    }

    // Limit decimal places to 2
    if (parts[1] && parts[1].length > 2) {
      return parts[0] + "." + parts[1].substring(0, 2)
    }

    return numericValue
  }

  const handleAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const formatted = formatAmount(e.target.value)
    setAmount(formatted)
    setError("")
  }

  const validateAmount = () => {
    const numAmount = Number.parseFloat(amount)
    if (!amount || isNaN(numAmount)) {
      setError("Please enter a valid amount between ₱1 and ₱50,000")
      return false
    }
    if (numAmount < 1) {
      setError("Please enter a valid amount between ₱1 and ₱50,000")
      return false
    }
    if (numAmount > 50000) {
      setError("Please enter a valid amount between ₱1 and ₱50,000")
      return false
    }
    return true
  }

  const generateBarcode = () => {
    if (!validateAmount()) return

    // Generate 24-character alphanumeric code
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    let code = "GC" // Prefix
    for (let i = 0; i < 22; i++) {
      code += characters.charAt(Math.floor(Math.random() * characters.length))
    }

    // Generate 8-digit reference code
    const referenceCode = Math.floor(10000000 + Math.random() * 90000000).toString()

    // Generate expiry date (24 hours from now)
    const expiryDate = new Date()
    expiryDate.setHours(expiryDate.getHours() + 24)
    const formattedExpiry =
      expiryDate.toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "long",
        year: "numeric",
      }) +
      " " +
      expiryDate.toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
      })

    setBarcodeData({
      code,
      referenceCode,
      expiryDate: formattedExpiry,
    })
    setStep("barcode")
  }

  // Generate real barcode when barcodeData changes
  useEffect(() => {
    if (barcodeData && barcodeRef.current && step === "barcode") {
      try {
        JsBarcode(barcodeRef.current, barcodeData.code, {
          format: "CODE128",
          width: 2,
          height: 60,
          displayValue: false,
          background: "#ffffff",
          lineColor: "#000000",
          margin: 0,
        })
      } catch (error) {
        console.error("Barcode generation failed:", error)
      }
    }
  }, [barcodeData, step])

  const copyToClipboard = async () => {
    if (barcodeData) {
      try {
        await navigator.clipboard.writeText(barcodeData.referenceCode)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
      } catch (err) {
        console.error("Failed to copy:", err)
      }
    }
  }

  const formatDisplayAmount = (amount: string) => {
    const num = Number.parseFloat(amount)
    if (isNaN(num)) return "0.00"
    return num.toLocaleString("en-PH", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })
  }

  if (step === "input") {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#004CFF] to-[#00A8FF] relative">
        {/* Mobile Status Bar Simulation */}
        <div className="h-6 bg-[#004CFF]" />

        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 text-white">
          <div className="flex items-center gap-3">
            <ArrowLeft className="w-6 h-6 cursor-pointer active:scale-95 transition-transform" />
            <h1 className="text-lg font-medium">Cash-In via Code</h1>
          </div>
          <Info className="w-6 h-6 cursor-pointer active:scale-95 transition-transform" />
        </div>

        {/* Content */}
        <div className="flex-1 bg-[#F8F9FA] rounded-t-3xl px-4 py-6 min-h-[calc(100vh-100px)]">
          <div className="max-w-sm mx-auto">
            <div className="text-center mb-8">
              <p className="text-[#6B7280] text-sm leading-relaxed px-4">
                Cash In made easier via Barcode or a unique Reference Code
              </p>
            </div>

            <div className="space-y-6">
              {/* Amount Input */}
              <div className="space-y-3">
                <div className="relative">
                  <div className="absolute left-4 top-1/2 transform -translate-y-1/2 text-[#6B7280] font-medium text-lg">
                    PHP
                  </div>
                  <Input
                    type="text"
                    inputMode="decimal"
                    value={amount}
                    onChange={handleAmountChange}
                    placeholder="Enter Amount"
                    className="pl-16 pr-4 py-4 text-xl font-medium border-0 bg-white rounded-2xl shadow-sm focus:ring-2 focus:ring-[#004CFF] text-[#1A1A1A] h-14"
                  />
                </div>
                {error && (
                  <div className="px-2">
                    <p className="text-[#EF4444] text-sm">{error}</p>
                  </div>
                )}
              </div>

              {/* Spacer */}
              <div className="flex-1 min-h-[200px]" />

              {/* Bottom Section */}
              <div className="space-y-4">
                <p className="text-[#6B7280] text-center text-sm px-4">Please check the amount before you proceed.</p>

                {/* Generate Button */}
                <Button
                  onClick={generateBarcode}
                  disabled={!amount || Number.parseFloat(amount) < 1}
                  className="w-full py-4 text-base font-semibold bg-gradient-to-r from-[#00A8FF] to-[#004CFF] hover:from-[#0096E6] hover:to-[#0040E6] disabled:opacity-50 disabled:cursor-not-allowed rounded-full h-14 active:scale-98 transition-transform"
                >
                  GENERATE CODE
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#004CFF] to-[#00A8FF] relative">
      {/* Mobile Status Bar Simulation */}
      <div className="h-6 bg-[#004CFF]" />

      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 text-white">
        <div className="flex items-center gap-3">
          <ArrowLeft
            className="w-6 h-6 cursor-pointer active:scale-95 transition-transform"
            onClick={() => setStep("input")}
          />
          <h1 className="text-lg font-medium">Cash-In via Code</h1>
        </div>
        <div className="w-6 h-6" />
      </div>

      {/* Content */}
      <div className="flex-1 bg-[#F8F9FA] rounded-t-3xl px-4 py-6 min-h-[calc(100vh-100px)] overflow-y-auto">
        <div className="max-w-sm mx-auto">
          <div className="text-center space-y-6">
            {/* Instructions */}
            <p className="text-[#6B7280] text-sm leading-relaxed px-2">
              Show one of these codes to the cashier of any participating merchant to Cash In.
            </p>

            {/* Amount Display */}
            <div className="space-y-1">
              <p className="text-[#6B7280] text-sm">the amount of</p>
              <p className="text-[#1A1A1A] text-2xl font-semibold">php {formatDisplayAmount(amount)}</p>
            </div>

            {/* Real Barcode */}
            <Card className="p-4 bg-white border border-[#e0e0e0] rounded-2xl shadow-sm">
              <div className="space-y-3">
                {/* SVG Barcode */}
                <div className="flex justify-center overflow-hidden">
                  <svg ref={barcodeRef} className="max-w-full h-auto" style={{ maxWidth: "280px" }} />
                </div>

                {/* Barcode Number */}
                <p className="text-xs font-mono text-center text-[#1A1A1A] tracking-wider break-all px-2">
                  {barcodeData?.code}
                </p>
              </div>
            </Card>

            {/* Reference Code */}
            <Card className="p-4 bg-white border-2 border-[#e0e0e0] rounded-2xl shadow-sm">
              <div className="flex items-center justify-between gap-3">
                <span className="text-xl font-mono text-[#6B7280] tracking-wider flex-1 text-center">
                  {barcodeData?.referenceCode}
                </span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={copyToClipboard}
                  className="text-[#004CFF] hover:bg-[#004CFF]/10 p-2 rounded-full active:scale-95 transition-transform flex-shrink-0"
                >
                  {copied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
                </Button>
              </div>
            </Card>

            {/* Validity */}
            <div className="space-y-1">
              <p className="text-[#6B7280] text-sm">valid until</p>
              <p className="text-[#6B7280] text-sm font-medium">{barcodeData?.expiryDate}</p>
            </div>

            {/* Branding */}
            <div className="text-center space-y-1 py-4">
              <h2 className="text-3xl font-bold text-[#1A1A1A]">GCash</h2>
              <p className="text-[#6B7280] text-lg">Cash In</p>
            </div>

            {/* Done Button */}
            <div className="pt-4 pb-6">
              <Button
                onClick={() => setStep("input")}
                className="w-full py-4 text-base font-semibold bg-gradient-to-r from-[#00A8FF] to-[#004CFF] hover:from-[#0096E6] hover:to-[#0040E6] rounded-full h-14 active:scale-98 transition-transform"
              >
                DONE
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

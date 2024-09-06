"use client"

import { useState } from "react";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

export function UiMain() {
  const [predictors, setPredictors] = useState({
    'Lot Size': 6000,
    'List Price': 500000,
    'Baths': 2,
    'Structure Type': '',  // Changed to a string
    'Beds': 3,
    'Square Footage': 1800,
    'HOA Fee': 200,
    'Stories': 2,
    'Attached Garage': true,
    'New Construction': false,
  });

  const [prediction, setPrediction] = useState({
    daysOnMarket: "Average",
    confidence: {
      Average: 0.7,
      Slow: 0.3,
    },
  });

  const handleInputChange = (field: string, value: any) => {
    setPredictors({
      ...predictors,
      [field]: value,
    });
  };

  const handleCalculate = async () => {
    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(predictors),
      });
      
      const data = await response.json();
      
      // Assuming response format:
      // { prediction: "average", probabilities: { "average": 0.8, "slow": 0.2 } }
      setPrediction({
        daysOnMarket: data.prediction,
        confidence: data.probabilities,  // Update confidence with the probabilities returned
      });
      
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }
  };
  

  return (
    <div className="flex flex-col h-screen">
      <header className="bg-primary text-primary-foreground py-4 px-6">
        <h1 className="text-2xl font-bold">Days on Market Predictor</h1>
      </header>
      <main className="flex-1 grid grid-cols-2 gap-8 p-8">
        <div className="bg-card rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold mb-4">Predictors</h2>
          <form className="grid grid-cols-2 gap-4">
            <div className="grid gap-2">
              <Label htmlFor="lotSize">Lot Size (sq ft)</Label>
              <Input
                id="lotSize"
                type="number"
                min={1000}
                max={100000}
                value={predictors['Lot Size']}
                onChange={(e) => handleInputChange("Lot Size", parseInt(e.target.value))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="listPrice">List Price</Label>
              <Input
                id="listPrice"
                type="number"
                min={100000}
                max={5000000}
                value={predictors['List Price']}
                onChange={(e) => handleInputChange("List Price", parseInt(e.target.value))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="baths">Baths</Label>
              <Input
                id="baths"
                type="number"
                min={1}
                max={10}
                value={predictors['Baths']}
                onChange={(e) => handleInputChange("Baths", parseInt(e.target.value))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="structureType">Structure Type (House, Triplex, MultiFamily)</Label>
              <Input
                id="structureType"
                type="text"
                value={predictors['Structure Type']}
                onChange={(e) => handleInputChange("Structure Type", e.target.value)}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="beds">Beds</Label>
              <Input
                id="beds"
                type="number"
                min={1}
                max={10}
                value={predictors['Beds']}
                onChange={(e) => handleInputChange("Beds", parseInt(e.target.value))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="sqft">Square Footage</Label>
              <Input
                id="sqft"
                type="number"
                min={500}
                max={10000}
                value={predictors['Square Footage']}
                onChange={(e) => handleInputChange("Square Footage", parseInt(e.target.value))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="hoaFee">HOA Fee</Label>
              <Input
                id="hoaFee"
                type="number"
                min={0}
                max={1000}
                value={predictors['HOA Fee']}
                onChange={(e) => handleInputChange("HOA Fee", parseInt(e.target.value))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="stories">Stories</Label>
              <Input
                id="stories"
                type="number"
                min={1}
                max={5}
                value={predictors['Stories']}
                onChange={(e) => handleInputChange("Stories", parseInt(e.target.value))}
              />
            </div>
            <div className="col-span-2 grid grid-cols-2 gap-4">
              <Label className="flex items-center gap-2">
                <Input
                  type="checkbox"
                  checked={predictors['Attached Garage']}
                  onChange={(e) => handleInputChange("Attached Garage", e.target.checked)}
                />
                Attached Garage
              </Label>
              <Label className="flex items-center gap-2">
                <Input
                  type="checkbox"
                  checked={predictors['New Construction']}
                  onChange={(e) => handleInputChange("New Construction", e.target.checked)}
                />
                New Construction
              </Label>
            </div>
            <div className="col-span-2 mt-4">
              <button
                type="button"
                className="bg-primary text-primary-foreground px-4 py-2 rounded"
                onClick={handleCalculate}
              >
                Calculate
              </button>
            </div>
          </form>
        </div>
        <div className="bg-card rounded-lg shadow-md p-6">
  <h2 className="text-xl font-bold mb-4">Prediction</h2>
  <div className="grid gap-4">
    <div>
      <h3 className="text-lg font-bold">Predicted Days on Market (Average is less than 45 days, Slow is greater than 45 days)</h3>
      <div className="text-4xl font-bold">{prediction.daysOnMarket}</div> {/* Show prediction */}
    </div>
    <div>
      <h3 className="text-lg font-bold">Confidence Levels</h3>
      <div className="grid gap-2">
        {Object.keys(prediction.confidence || {}).map((key) => (
          <div key={key} className="flex items-center justify-between">
            <span>{key}</span>
            <div className="w-full bg-muted rounded-full h-4 mr-2">
              <div
                className="bg-primary h-full rounded-full"
                style={{ width: `${prediction.confidence[key] * 100}%` }}  // Display progress bar
              />
            </div>
            <span>{(prediction.confidence[key] * 100).toFixed(0)}%</span>  {/* Show percentage */}
          </div>
        ))}
      </div>
    </div>
  </div>
</div>

      </main>
    </div>
  );
}

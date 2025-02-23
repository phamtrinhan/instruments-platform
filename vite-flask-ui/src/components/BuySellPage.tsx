import React, { useState } from "react";
import {
  Box,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Snackbar,
  Alert,
} from "@mui/material";

interface BuySellPageProps {
  stockSymbol: string;
  stockPrice: number;
}

const BuySellPage: React.FC<BuySellPageProps> = ({ stockSymbol, stockPrice }) => {
  const [quantity, setQuantity] = useState<number | string>("");
  const [action, setAction] = useState<"buy" | "sell" | null>(null);
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  const handleBuy = () => {
    setAction("buy");
    setSnackbarOpen(true);
  };

  const handleSell = () => {
    setAction("sell");
    setSnackbarOpen(true);
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
    setAction(null);
  };

  const totalCost = typeof quantity === "number" ? quantity * stockPrice : 0;
  const isQuantityValid = quantity && Number(quantity) > 0;

  return (
    <Box sx={{ padding: 4, maxWidth: 600, margin: "0 auto" }}>
      <Card>
        <CardContent>
          <Typography variant="h4" align="center" gutterBottom>
            {stockSymbol} - ${stockPrice.toFixed(2)}
          </Typography>
          <Typography variant="subtitle1" align="center" gutterBottom>
            Buy or Sell Stocks
          </Typography>
          <TextField
            label="Quantity"
            type="number"
            fullWidth
            value={quantity}
            onChange={(e) => setQuantity(Number(e.target.value) || "")}
            variant="outlined"
            sx={{ marginY: 2 }}
          />
          <Typography variant="h6" align="center" gutterBottom>
            Total: ${totalCost.toFixed(2)}
          </Typography>
          <Box display="flex" justifyContent="space-between" mt={2}>
            <Button
              variant="contained"
              color="success"
              fullWidth
              onClick={handleBuy}
              disabled={!isQuantityValid}
              sx={{ marginRight: 1 }}
            >
              Buy
            </Button>
            <Button
              variant="contained"
              color="error"
              fullWidth
              onClick={handleSell}
              disabled={!isQuantityValid}
            >
              Sell
            </Button>
          </Box>
        </CardContent>
      </Card>
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={action === "buy" ? "success" : "info"}
          sx={{ width: "100%" }}
        >
          {action === "buy"
            ? `Successfully bought ${quantity} shares of ${stockSymbol}!`
            : `Successfully sold ${quantity} shares of ${stockSymbol}!`}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default BuySellPage;

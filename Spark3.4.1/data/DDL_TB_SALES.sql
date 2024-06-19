-- TB_SALES definition

CREATE TABLE `TB_SALES` (
  `Sale_Date` varchar(8) NOT NULL,
  `Transaction_ID` varchar(20) NOT NULL,
  `Product_ID` varchar(50) NOT NULL,
  `Customer_ID` varchar(20) NOT NULL,
  `Quantity_Sold` int(11) NOT NULL,
  `Sales_Revenue` int(11) NOT NULL,
  `Cost_Price_per_Unit` int(11) NOT NULL,
  `Selling_Expenses` int(11) NOT NULL,
  `Employee_ID` int(11) NOT NULL,
  `Channel_CD` varchar(10) NOT NULL,
  KEY `TB_SALES_Sale_Date_IDX` (`Sale_Date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

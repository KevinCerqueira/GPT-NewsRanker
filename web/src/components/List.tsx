// src/components/List.tsx
// src/components/List.tsx
import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Link,
  Chip,
  Grid,
  Container,
  Button,
  Box,
  TextField,
} from "@mui/material";
// import { DateRangePicker, MobileDateRangePicker, DesktopDateRangePicker } from '@mui/lab';
import { DateRangePicker } from "@mui/lab";
import AdapterDateFns from "@mui/lab/AdapterDateFns";
import { styled } from "@mui/system";
import dayjs, { Dayjs } from "dayjs";
import { DemoContainer } from "@mui/x-date-pickers/internals/demo";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
// import { DateRangeTextFieldProps } from "@mui/lab/DateRangePicker";
interface Item {
  id: string;
  title: string;
  description: string;
  date: string;
  score: number;
  image: string;
  link: string;
}

interface ListItemProps extends Item {}

const ScoreChip = styled(Chip)<{ score: number }>(({ score }) => ({
  backgroundColor: `rgb(${255 * (1 - score / 10)}, ${255 * (score / 10)}, 0)`,
}));

const StyledCard = styled(Card)(({ theme }) => ({
  height: "100%",
  display: "flex",
  flexDirection: "column",
  position: "relative",
  "& .MuiChip-root": {
    position: "absolute",
    top: theme.spacing(2),
    right: theme.spacing(2),
  },
}));

const ListItem: React.FC<ListItemProps> = ({
  id,
  title,
  description,
  date,
  score,
  image,
  link,
}) => {
  return (
    <StyledCard>
      <ScoreChip label={`Avaliação: ${score}`} score={score} />
      <CardContent sx={{ flexGrow: 1, paddingTop: "60px" }}>
        <Typography variant="h5" component="div">
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {description}
        </Typography>
      </CardContent>
      <CardMedia component="img" height="140" image={image} alt={title} />
      <CardContent>
        <Button
          variant="contained"
          color="primary"
          href={link}
          target="_blank"
          rel="noopener noreferrer"
        >
          Visite o site
        </Button>
      </CardContent>
      <Box
        sx={{
          p: 1,
          display: "flex",
          justifyContent: "center",
          backgroundColor: "action.selected",
        }}
      >
        <Typography variant="body2" color="text.secondary">
          Data: {date}
        </Typography>
      </Box>
    </StyledCard>
  );
};
type DateRange = [Date | null, Date | null];
const List: React.FC = () => {
  const [items, setItems] = useState<Item[]>([]);
  const [descriptionFilter, setDescriptionFilter] = useState("");
  const [dateRange, setDateRange] = useState<DateRange>([
    new Date(),
    new Date(),
  ]);
  const [orderScore, setOrderScore] = useState("");
  const [value, setValue] = React.useState<Dayjs | null>(dayjs());
  const toggleOrderScore = () => {
    setOrderScore((prevOrderScore) =>
      prevOrderScore === "asc" ? "desc" : "asc"
    );
  };

  useEffect(() => {
    let params: any = {
      description: descriptionFilter,
      order_score: orderScore === "" ? "desc" : orderScore,
    };
    // if (dateRange[0]) {
    //   let params: any = {
    //     description: descriptionFilter,
    //     date_start: dateRange[0] ? dateRange[0].toISOString() : null,
    //     date_end: dateRange[1] ? dateRange[1].toISOString() : null,
    //     order_score: orderScore,
    //   };
    // }
    axios
      .get("https://api-newsranker.onrender.com/news", {
        params,
      })
      .then((response) => {
        setItems(response.data.data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, [descriptionFilter, dateRange, orderScore]);

  return (
    <Container>
      <Typography variant="h2" align="center" gutterBottom>
        NewsRanker
      </Typography>

      <Box sx={{ marginBottom: 2 }}>
        <TextField
          label="Pesquisa"
          variant="outlined"
          value={descriptionFilter}
          onChange={(e) => setDescriptionFilter(e.target.value)}
        />
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DemoContainer components={["DatePicker", "DatePicker"]}>
            <DatePicker label="Início" defaultValue={dayjs()} />
            <DatePicker
              label="Final"
              value={value}
              onChange={(newValue) => setValue(newValue)}
            />
          </DemoContainer>
        </LocalizationProvider>
        <Button onClick={toggleOrderScore}>
          Ordenar por score:{" "}
          {orderScore === "asc" ? "crescente" : "decrescente"}
        </Button>
      </Box>

      <Grid container spacing={3}>
        {items.map((item) => (
          <Grid item key={item.id} xs={12} sm={6} md={4}>
            <ListItem
              id={item.id}
              title={item.title}
              description={item.description}
              date={item.date}
              score={item.score}
              image={item.image}
              link={item.link}
            />
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default List;

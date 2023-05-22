import React, { useState, useEffect } from "react";
import axios from "axios";
import { styled } from "@mui/system";
import dayjs, { Dayjs } from "dayjs";
import "dayjs/locale/pt-br";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { ArrowUpward, ArrowDownward } from "@mui/icons-material";
import { Select, MenuItem } from "@mui/material";
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Chip,
  Grid,
  Container,
  Button,
  Box,
  TextField,
  IconButton,
  FormControl,
  CircularProgress,
} from "@mui/material";
import Item from "../types/Item";
interface ListItemProps extends Item {}
dayjs.locale("pt-br");

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
const StyledBody = styled("body")({
  backgroundColor: "#167CA3",
  margin: 0,
  padding: 0,
});
const ListItem: React.FC<ListItemProps> = ({
  id,
  title,
  description,
  date,
  score,
  imageUrl,
  newsUrl,
}) => {
  return (
    <StyledCard>
      <ScoreChip label={`Índice: ${score}`} score={score} />
      <CardContent sx={{ flexGrow: 1, paddingTop: "60px" }}>
        <Typography variant="h5" component="div">
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {description}
        </Typography>
      </CardContent>
      <CardMedia component="img" height="140" image={imageUrl} alt={title} />
      <CardContent>
        <Button
          variant="contained"
          color="primary"
          href={newsUrl}
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
          {date}
        </Typography>
      </Box>
    </StyledCard>
  );
};

const List: React.FC = () => {
  const [items, setItems] = useState<Item[]>([]);
  const [descriptionFilter, setDescriptionFilter] = useState("");
  const [startDate, setStartDate] = useState<Dayjs | string | null>(
    dayjs().subtract(7, "day")
  );
  const [finalDate, setFinalDate] = useState<Dayjs | string | null>(dayjs());
  const [orderScore, setOrderScore] = useState("desc");
  const [limit, setLimit] = useState(25);
  const [request, setRequest] = useState(0);
  const [requestError, setRequestError] = useState(false);
  const [messageError, setMessageError] = useState("");
  const [scoreFilter, setScoreFilter] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  const toggleOrderScore = () => {
    setOrderScore((prevOrderScore) =>
      prevOrderScore === "asc" ? "desc" : "asc"
    );
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const startDateFormatted = startDate
          ? dayjs(startDate).format("YYYY-MM-DD 00:00:00")
          : "";
        const finalDateFormatted = finalDate
          ? dayjs(finalDate).format("YYYY-MM-DD 23:59:59")
          : "";

        const params = {
          description: descriptionFilter,
          date_start: startDateFormatted,
          date_end: finalDateFormatted,
          score: scoreFilter,
          order_score: orderScore === "" ? "desc" : orderScore,
          limit: limit,
        };

        const response = await axios.get("https://api-newsranker.onrender.com/news", {
          params,
        });

        setRequest((prevRequest) => prevRequest + 1);

        if (!response.data.success) {
          setRequestError(true);
          setMessageError(response.data.error);
          setRequest(0);
          console.log(response.data);
          return;
        } else {
          setRequestError(false);
        }

        const newItems = response.data.data;

        console.log(limit);
        setItems(newItems);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [descriptionFilter, startDate, finalDate, orderScore, limit, scoreFilter]);

  const handleLoadMore = () => {
    const newLimit = items.length === 0 ? 25 : items.length + 25;
    setLoading(true);
    setLimit(newLimit);
  };

  return (
    <StyledBody>
      <Container
        sx={{
          backgroundColor: "#167CA3",
          display: "flex",
          flexDirection: "column",
          flexGrow: 1,
        }}
      >
        <Box
          sx={{
            height: "100vh",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <Box
            sx={{
              textAlign: "center",
              marginTop: "30px",
              marginBottom: "30px",
            }}
          >
            <Typography
              variant="h2"
              sx={{
                fontFamily: "'Arial', sans-serif",
                fontWeight: "bold",
                color: "#FFF",
                letterSpacing: "2px",
                marginBottom: "10px",
              }}
            >
              IPoN
              <img
                src="https://www.acordacidade.com.br/wp-content/uploads/2022/05/header-logo.png"
                alt="Logo"
                style={{ height: "50px" }}
              />
            </Typography>
            <Typography
              variant="h6"
              sx={{
                fontFamily: "'Arial', sans-serif",
                fontWeight: "normal",
                color: "#FFF",
                letterSpacing: "1px",
              }}
            >
              Índice de Positividade de Notícias do Acorda Cidade
            </Typography>
          </Box>

          <Box
            sx={{
              backgroundColor: "#FFF",
              borderRadius: "8px",
              marginBottom: 2,
              display: "flex",
              padding: 2,
              flexDirection: "column",
            }}
          >
            <TextField
              label="Pesquisa"
              variant="outlined"
              value={descriptionFilter}
              onChange={(e) => setDescriptionFilter(e.target.value)}
              sx={{ marginBottom: 2 }}
            />
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                marginBottom: 2,
              }}
            >
              <LocalizationProvider dateAdapter={AdapterDayjs} locale="pt-br">
                <DatePicker
                  label="Início"
                  value={startDate}
                  onChange={(date) => setStartDate(date)}
                  format="DD/MM/YYYY"
                  maxDate={finalDate || dayjs()}
                  sx={{ marginRight: 2 }}
                  closeOnSelect={true}
                />
                <DatePicker
                  label="Final"
                  value={finalDate}
                  onChange={(date) => setFinalDate(date)}
                  format="DD/MM/YYYY"
                  minDate={startDate || dayjs().subtract(7, "day")}
                  sx={{ marginRight: 2 }}
                  closeOnSelect={true}
                />
              </LocalizationProvider>
              <Typography variant="body1" sx={{ marginRight: 2 }}>
                Indíce:{" "}
              </Typography>
              <FormControl sx={{ minWidth: 30, marginBottom: 0 }}>
                <Select
                  sx={{ paddingTop: 0, height: "40px" }}
                  value={scoreFilter || ""}
                  onChange={(e) => {
                    const value = e.target.value;
                    if (value === "") {
                      setScoreFilter(null);
                    } else {
                      setScoreFilter(Number(value));
                    }
                  }}
                >
                  <MenuItem value="">
                    <em>Nenhum</em>
                  </MenuItem>
                  {Array.from({ length: 10 }, (_, i) => i + 1).map((num) => (
                    <MenuItem key={num} value={num}>
                      {num}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <IconButton
                onClick={toggleOrderScore}
                sx={{
                  backgroundColor: "transparent",
                  padding: 0,
                  "&:hover": {
                    backgroundColor: "transparent",
                  },
                }}
              >
                {orderScore === "asc" ? (
                  <ArrowUpward sx={{ fontSize: 32 }} />
                ) : (
                  <ArrowDownward sx={{ fontSize: 32 }} />
                )}
              </IconButton>
            </Box>
          </Box>

          <Box>
            <Grid container spacing={3}>
              {items.map((item) => (
                <Grid item key={item.id} xs={12} sm={6} md={4}>
                  <ListItem
                    id={item.id}
                    title={item.title}
                    description={item.description}
                    date={dayjs(item.date).format("DD/MM/YYYY HH:mm")}
                    score={item.score}
                    imageUrl={item.imageUrl}
                    newsUrl={item.newsUrl}
                  />
                </Grid>
              ))}
            </Grid>

            {items.length !== 0 && (
              <Button
                onClick={handleLoadMore}
                variant="contained"
                color="primary"
                disabled={loading}
                sx={{
                  marginTop: 3,
                  marginBottom: 3,
                  border: "2px solid #FFF",
                  color: "#FFF",
                }}
              >
                {loading ? <CircularProgress size={24} /> : "Carregar mais"}
              </Button>
            )}

            {requestError && (
              <Typography variant="body1" align="center">
                Houve um erro ao carregar os dados: {messageError}
              </Typography>
            )}
          </Box>
        </Box>
      </Container>
    </StyledBody>
  );
};

export default List;

// Parámetros del modelo
int t = getHour() * 60 + getMinute() * 60 + getSecond();

double k_max_LS = 4.16;       // Tasa máxima de producción de grelina (en pM/min)
double lambda_LS = 0.00462;   // Tasa de disminución de la secreción de grelina en función del contenido gástrico (1/g)
double k_XL = 0.02;           // Tasa de eliminación de grelina del torrente sanguíneo (1/min)
double k_XG = 0.0072;         // Tasa aparente de eliminación de glucosa en condiciones normales (1/min)
double k_XGE = 0.0036;        // Tasa adicional de eliminación de glucosa durante actividad física (1/min)
double k_G = 0.4464;          // Tasa constante de entrada de glucosa en plasma desde el hígado (mmol/min)
double rho_GS = 0.9;          // Fracción de glucosa en los alimentos que es realmente absorbida por el intestino
double eta_G = 0.2;           // Contribución de los alimentos al nivel de glucosa en sangre (g glucosa/g alimento)
double V_G = 12.4;            // Volumen de distribución de la glucosa en el cuerpo (litros)
double A_max = 50;            // Valor máximo de apetito en unidades arbitrarias
double L_A50 = 120;           // Concentración de grelina en plasma cuando el apetito alcanza el 50% de su máximo (pM)
double lambda_AG = 0.3;       // Factor que representa la reducción del apetito debido a un aumento en la glucosa (1/mM)
double k_XS = 0.0154;         // Tasa de vaciamiento gástrico (1/min)
double k_S = 16.5;            // Tasa de ingesta de alimentos cuando la persona está comiendo (g/min)
double S_50 = 150;            // Contenido gástrico al cual la secreción de grelina se reduce al 50% de su máximo (g)
double L_ss = 178;            // Nivel de grelina en estado estable durante el ayuno (pM)
double G_ss = 5;              // Concentración de glucosa en estado estable en condiciones normales (mM)

// Configuración de simulación
double t_start = 17 * 60;  // Inicio del día en minutos
double t_end = 22 * 60;    // Fin del día en minutos
double dt = 1;   

// Horarios de comida en minutos desde la medianoche
List<Integer> meal_times = Arrays.asList(8 * 60, 13 * 60, 18 * 60);
    
// Duración de cada comida en minutos
int meal_duration = 30;

int H = habitos(t, meal_times, meal_duration); // Hábitos alimenticios

// Variable externa que influye en el apetito
boolean influenciadoPorOlor = true;

// Apetito
double factorOlor = influenciadoPorOlor ? 1.2 : 1.0; // Incrementa el apetito en un 20% si hay influencia del olor

A = A_max * (L / (L_A50 + L)) * Math.exp(-lambda_AG * G) * factorOlor;

// Estado de ingesta
//chi_intake = (yaConsumioComida) ? 13 : 0;
chi_intake = (yaConsumioComida || A > 200 * factorOlor) ? 1 : 0;

// Grelina
//double dL = k_max_LS * Math.exp(-lambda_LS * S) - k_XL * L;
double dL = k_max_LS * Math.exp(-lambda_LS * S) * factorOlor - k_XL * L;

L += dL * dt;

// Glucosa
double dG = -(k_XG + k_XGE * E) * G + (k_G + k_XS * eta_G * rho_GS * S) / V_G;
G += dG * dt;

// Contenido gástrico
//double dS = -k_XS * S + k_S * chi_intake;
double k_S_ajustado = k_S * factorOlor;
double dS = -k_XS * S + k_S_ajustado * chi_intake;

S += dS * dt;
if (S < 0) {
    S = 0;
}



public boolean tieneApetito() {
    // Factores internos 120, 4, 50
    boolean grelinaAlta = L > 120; // Comparar con un nivel umbral de grelina
    boolean glucosaBaja = G < 1.2; // Comparar con un nivel umbral de glucosa
    boolean estomagoVacio = S < 100; // Comparar con un contenido gástrico umbral

    // Factor externo
    boolean estimuladoPorOlor = influenciadoPorOlor;

    // Determinar si hay hambre
    return grelinaAlta && glucosaBaja && estomagoVacio;
}

public boolean tieneApetito(){
    this.calcularApetito();

    if(S <=  150){
        return true;
    }else{
        return false;
        }

}
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
    boolean grelinaAlta = L > 90; // Comparar con un nivel umbral de grelina
    boolean glucosaBaja = G < 4; // Comparar con un nivel umbral de glucosa
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


public int calcularToleranciaFila(double nivelGrelina, double nivelGlucosa, double contenidoGastrico) {
    // Umbrales para ajustar la percepción de hambre
    double umbralGrelinaAlta = 120; // Nivel alto de grelina (en pM)
    double umbralGlucosaBaja = 4.0; // Nivel bajo de glucosa (en mM)
    double umbralContenidoGastricoBajo = 50; // Contenido gástrico bajo (en g)

    // Ponderación para calcular la sensación de hambre (valores ajustables)
    double pesoGrelina = 0.5; // La grelina tiene una gran influencia en la sensación de hambre
    double pesoGlucosa = 0.3; // La glucosa tiene una influencia moderada
    double pesoContenidoGastrico = 0.2; // El contenido gástrico tiene una menor influencia

    // Normalización de las variables (entre 0 y 1)
    double hambreGrelina = Math.min(1.0, nivelGrelina / umbralGrelinaAlta); // Máximo 1.0
    double hambreGlucosa = Math.min(1.0, Math.max(0.0, (umbralGlucosaBaja - nivelGlucosa) / umbralGlucosaBaja));
    double hambreContenidoGastrico = Math.min(1.0, Math.max(0.0, (umbralContenidoGastricoBajo - contenidoGastrico) / umbralContenidoGastricoBajo));

    // Calcular una "puntuación de hambre" ponderada
    double puntuacionHambre = (hambreGrelina * pesoGrelina) +
                              (hambreGlucosa * pesoGlucosa) +
                              (hambreContenidoGastrico * pesoContenidoGastrico);

    // Convertir la puntuación de hambre a una tolerancia de fila
    int maxFila = 20; // Máximo número de personas en la fila
    int minFila = 1;  // Mínimo número de personas en la fila
    int toleranciaFila = (int) Math.round(minFila + puntuacionHambre * (maxFila - minFila));

    return toleranciaFila;
}


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Parámetros del modelo
int t = getHour()*60 + getMinute()*60 +getSecond();

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

// Apetito
A = A_max * (L / (L_A50 + L)) * Math.exp(-lambda_AG * G);

// Estado de ingesta
//chi_intake = (H == 1 || A > 200) ? 1 : 0;  // Se come si hay hábito o el apetito es alto
chi_intake = (yaConsumioComida) ? 13: 0;

// Grelina
double dL = k_max_LS * Math.exp(-lambda_LS * S) - k_XL * L;
L += dL * dt;

// Glucosa
double dG = -(k_XG + k_XGE * E) * G + (k_G + k_XS * eta_G * rho_GS * S) / V_G;
G += dG * dt;

// Contenido gástrico
double dS = -k_XS * S + k_S * chi_intake;
S += dS * dt;
if (S < 0) {
    S = 0;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


import java.util.Random;

public void randomApetito() {
    Random rand = new Random();
    String[] states = {"fed", "fasting"}; 
    String initial_state = states[rand.nextInt(2)]; // Selecciona estado inicial al azar

    // Declaración de variables de niveles
    double nivelGrelina;    // Nivel de grelina en pM
    double nivelGlucosa;    // Nivel de glucosa en mM
    double contenidoGastrico; // Contenido gástrico en g

    // Asignación de niveles según el estado
    if (initial_state.equals("fed")) {
        contenidoGastrico = 300; // Estómago lleno (en g)
        nivelGrelina = 50 + rand.nextDouble() * 20; // Grelina baja (50-70 pM)
        nivelGlucosa = 5.5 + rand.nextDouble() * 1.5; // Glucosa moderada (5.5-7.0 mM)
        yaConsumioComida = true;
    } else { // fasting
        contenidoGastrico = 0; // Estómago vacío
        nivelGrelina = 150 + rand.nextDouble() * 30; // Grelina alta (150-180 pM)
        nivelGlucosa = 3.0 + rand.nextDouble() * 1.0; // Glucosa baja (3.0-4.0 mM)
        yaConsumioComida = false;
    }

    // Asignar niveles al agente
    this.S = contenidoGastrico; 
    this.L = nivelGrelina; 
    this.G = nivelGlucosa;

    // Determinar cuántas personas puede esperar en fila
    int min = 30;
    int max = 150;
    this.umbralPersonasAEsperar = rand.nextInt((max - min) + 1) + min;

    // Mostrar los valores generados
    System.out.println("Estado inicial: " + initial_state);
    System.out.println("Contenido gástrico (S): " + contenidoGastrico + " g");
    System.out.println("Nivel de grelina (L): " + nivelGrelina + " pM");
    System.out.println("Nivel de glucosa (G): " + nivelGlucosa + " mM");
    System.out.println("Personas dispuestas a esperar en fila: " + umbralPersonasAEsperar);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
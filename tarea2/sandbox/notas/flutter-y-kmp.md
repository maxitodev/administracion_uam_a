# Flutter y Kotlin Multiplatform

Los dos repositorios de ejemplo hacen lo mismo, un «Hola Mundo» para Android e iOS,
pero comparten código de forma distinta:

- **HolaMundoFlutter** se escribe en Dart. Flutter dibuja la interfaz con sus propios
  widgets y genera las carpetas nativas `android/` e `ios/`. Se corre con `flutter run`.
- **HolaMundoKMP** se escribe en Kotlin. El módulo `shared` tiene el código común y la
  interfaz en Compose Multiplatform; `androidApp` es una app Android normal. Se compila
  con Gradle y se corre desde Android Studio.

Lo que cambia por plataforma: en Flutter se consulta `Platform`; en KMP se declara una
función `expect` en `commonMain` y cada plataforma escribe su `actual`.

declare const marca: unique symbol;

/**
 * Tipo con marca nominal: `Marca<string, "Email">` no se puede construir con un
 * `string` cualquiera, solo con la función que lo valida (el *newtype* de Rust).
 */
export type Marca<T, M extends string> = T & { readonly [marca]: M };

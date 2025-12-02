const BUCKET_URL = "https://storage.googleapis.com/img-tienda-nuva";

products = [
    {
        "sku": 'NK-001',
        "title": 'Ojotas de tibron',
        "description": 'Ojotas grises con diseño de tibron',
        "price": 8500,
        "category": 'niño',
        "image": `${BUCKET_URL}/sharki-1g.jpg.avif`
    },
    {
        "sku": 'NK-002',
        "title": 'Sharki con luces',
        "description": 'Sharki con luces y diseño de tibron',
        "price": 6200,
        "category": 'niño',
        "image": `${BUCKET_URL}/sharki-2g.jpg.avif`
    },
    {
        "sku": 'NK-003',
        "title": 'Remera Estampada',
        "description": 'Remera de algodón con diseños divertidos',
        "price": 3500,
        "category": 'niño',
        "image": 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=400&h=300&fit=crop'
    },
    {
        "sku": 'NK-004',
        "title": 'Pantalón Deportivo',
        "description": 'Pantalón cómodo ideal para deportes y juegos',
        "price": 4800,
        "category": 'niño',
        "image": 'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400&h=300&fit=crop'
    },
    {
        "sku": 'NA-001',
        "title": 'Vestido Floreado',
        "description": 'Hermoso vestido con estampado de flores',
        "price": 7200,
        "category": 'niña',
        "image": 'https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=400&h=300&fit=crop'
    },
    {
        "sku": 'NA-002',
        "title": 'Zapatillas Brillantes',
        "description": 'Zapatillas con detalles brillantes y luces',
        "price": 9500,
        "category": 'niña',
        "image": 'https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=400&h=300&fit=crop'
    },
    {
        "sku": 'NA-003',
        "title": 'Conjunto de Verano',
        "description": 'Conjunto fresco y colorido para el verano',
        "price": 5800,
        "category": 'niña',
        "image": 'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400&h=300&fit=crop'
    },
    {
        "sku": 'NA-004',
        "title": 'Mochila Unicornio',
        "description": 'Mochila con diseño de unicornio y brillos',
        "price": 6800,
        "category": 'niña',
        "image": 'https://images.unsplash.com/photo-1577655197620-704858b270ac?w=400&h=300&fit=crop'
    },
    {
        "sku": 'NK-005',
        "title": 'Gorra Deportiva',
        "description": 'Gorra ajustable con protección UV',
        "price": 2500,
        "category": 'niño',
        "image": 'https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400&h=300&fit=crop'
    },
    {
        "sku": 'NA-005',
        "title": 'Diadema con Moño',
        "description": 'Diadema decorativa con moño elegante',
        "price": 1800,
        "category": 'niña',
        "image": 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=400&h=300&fit=crop'
    },
    {
        "sku": 'NK-006',
        "title": 'Camiseta de Fútbol',
        "description": 'Camiseta transpirable para jugar al fútbol',
        "price": 4200,
        "category": 'niño',
        "image": 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=400&h=300&fit=crop'
    },
    {
        "sku": 'NK-007',
        "title": 'Camisa de algodon',
        "description": 'hermosa camisa de algodon',
        "price": 400,
        "category": 'niño',
        "image": 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=400&h=300&fit=crop'
    }
]

// Función para optimizar carga de imágenes
function optimizeImageLoading() {
    // Precargar imágenes críticas
    const criticalImages = [
        `${BUCKET_URL}/sharki-1g.jpg.avif`,
        `${BUCKET_URL}/sharki-2g.jpg.avif`
    ];
    
    criticalImages.forEach(src => {
        const img = new Image();
        img.src = src;
    });
}
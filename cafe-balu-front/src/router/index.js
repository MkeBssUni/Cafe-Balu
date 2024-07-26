import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
    {
        path: "/",
        redirect: "/home",
    },
    {
        path: "/",
        component: {
            render(c) {
                return c("router-view");
            },
        },
        children: [
            {
                path: "/home",
                name: "home",
                component: () => import("../views/Home.vue"),
            },
            {
                path: "/menu",
                name: "menu",
                component: () => import("../views/Menu.vue"),
            },
            {
                path: "/login",
                name: "login",
                component: () => import("../modules/auth/views/Login.vue"),
                meta: {
                    hideNavigation: true,
                }
            },            
            {
                path: "/validate-password",
                name: "validatePassword",
                component: () => import("../modules/auth/views/ValidatePassword.vue"),
                meta: {
                    hideNavigation: true,
                }
            },
            {
                path: "/products",
                name: "products",
                component: () => import("../modules/products/views/Products.vue"),
            },
            {
                path: "/sales",
                name: "sales",
                component: () => import("../modules/sales/views/Sales.vue"),
            },
            {
                path: "/categories",
                name: "categories",
                component: () => import("../modules/categories/views/Categories.vue"),
            },
        ],
    },
];

const router = new VueRouter({ routes });
export default router;
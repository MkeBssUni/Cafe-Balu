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
                path: "/login",
                name: "login",
                component: () => import("../modules/auth/views/Login.vue"),
                meta: {
                    hideNavigation: true,
                }
            },
            {
                path: "/products",
                name: "products",
                component: () => import("../modules/products/views/Products.vue"),
            },
        ],
    },
];

const router = new VueRouter({ routes });
export default router;